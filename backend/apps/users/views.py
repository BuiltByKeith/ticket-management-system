from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.utils.responses import success_response, error_response
from .models import User
from .serializers import LoginSerializer, UserReadSerializer, UserWriteSerializer
from apps.utils.permissions import IsAdmin, IsAdminOrDeveloper

# Create your views here.


class LoginView(APIView):
    """
    Public endpoint - no authentication required.
    Accepts email and password, returns JWT access and refresh tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Authenticate() checks the credentials against the database
        # Returns None if credentials are invalid
        user = authenticate(request, username=email, password=password)

        if user is None:
            return error_response(
                message="Invalid email or password",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return error_response(
                message="This account has been deactivated",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return success_response(
            message="Login Successfull.",
            data={
                "user": UserReadSerializer(user).data,
                "tokens": {
                    "access": str(access),
                    "refresh": str(refresh),
                },
            },
        )


class RefreshTokenView(APIView):
    """
    Pulibc endpoint.
    Accepts a refresh token, returns a new access token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return error_response(
                message="Refresh token is required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            return success_response(
                message="Token refresh successfully!",
                data={
                    "access": str(refresh.access_token),
                },
            )
        except TokenError:
            return error_response(
                message="Invalide or expired refresh token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    Protected endpoint - required authentication.
    Blacklists the refresh token so it can no longer be used.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return error_response(
                message="Refresh token is required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return success_response(message="Logged out successfully.")
        except TokenError:
            return error_response(
                message="Invalid or expired refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class MeView(APIView):
    """
    Protected endpoint.
    Returns the currently authenticated user's profile.
    Useful for the frontend to know who is logged in after page refresh.
    """

    permissions_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserReadSerializer(request.user)
        return success_response(
            message="User Profile retrieved successfully.", data=serializer.data
        )


class UserListCreateView(APIView):
    """
    GET  /api/v1/users/   — list all users (admin only)
    POST /api/v1/users/   — create a user (admin only)
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserReadSerializer(users, many=True)
        return success_response(
            message="Users retrieved successfully.", data=serializer.data
        )

    def post(self, request):
        serializer = UserWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return success_response(
            message="User created successfully.",
            data=UserReadSerializer(user).data,
            status_code=status.HTTP_201_CREATED,
        )


class UserDetailView(APIView):
    """
    GET    /api/v1/users/<ulid>/   — retrieve a user (admin only)
    PUT    /api/v1/users/<ulid>/   — full update (admin only)
    PATCH  /api/v1/users/<ulid>/   — partial update (admin only)
    DELETE /api/v1/users/<ulid>/   — delete a user (admin only)
    """

    permission_classes = [IsAdmin]

    def get_object(self, ulid):
        try:
            return User.objects.get(ulid=ulid)
        except User.DoesNotExist:
            return None

    def get(self, request, ulid):
        user = self.get_object(ulid)
        if user is None:
            return error_response(
                message="User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = UserReadSerializer(user)
        return success_response(
            message="User retrieved successfully.", data=serializer.data
        )

    def put(self, request, ulid):
        user = self.get_object(ulid)
        if user is None:
            return error_response(
                message="User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = UserWriteSerializer(user, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return success_response(
            message="User updated successfully.", data=UserReadSerializer(user).data
        )

    def patch(self, request, ulid):
        user = self.get_object(ulid)
        if user is None:
            return error_response(
                message="User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = UserWriteSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return success_response(
            message="User updated successfully.", data=UserReadSerializer(user).data
        )

    def delete(self, request, ulid):
        user = self.get_object(ulid)
        if user is None:
            return error_response(
                message="User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        user.delete()
        return success_response(message="User deleted successfully.")
