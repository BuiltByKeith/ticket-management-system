from rest_framework.views import APIView
from rest_framework import status

from apps.utils.responses import success_response, error_response
from apps.utils.permissions import IsAdmin, IsAdminOrDeveloper
from .models import ConcernType
from .serializers import ConcernTypeSerializer


class ConcernTypeListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]

    def get(self, request):
        concern_types = ConcernType.objects.all()
        serializer = ConcernTypeSerializer(concern_types, many=True)

        return success_response(
            message="Concern types retrieved successfully!", data=serializer.data
        )

    def post(self, request):
        serializer = ConcernTypeSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Concern type created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class ConcernTypeDetailView(APIView):
    
    # Get permissions if the authenticated user is admin or not
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]


    # Find the object (data) that corresspond with the given ULID from the client and validates if it exists
    def get_object(self, ulid):
        try:
            return ConcernType.objects.get(ulid=ulid)
        except ConcernType.DoesNotExist:
            return None

    # if the ULID exists, use that ULID to get the concern types
    def get(self, request, ulid):
        concern_type = self.get_object(ulid)
        if concern_type is None:
            return error_response(
                message="Concern type not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = ConcernTypeSerializer(concern_type)
        return success_response(
            message="Concern type retrieved successfully.", data=serializer.data
        )

    
    def put(self, request, ulid):
        concern_type = self.get_object(ulid)
        if concern_type is None:
            return error_response(
                message="Concern type not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = ConcernTypeSerializer(concern_type, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Concern type updated successfully.", data=serializer.data
        )

    def patch(self, request, ulid):
        concern_type = self.get_object(ulid)
        if concern_type is None:
            return error_response(
                message="Concern type not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = ConcernTypeSerializer(
            concern_type, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Concern type updated successfully.", data=serializer.data
        )

    def delete(self, request, ulid):
        concern_type = self.get_object(ulid)
        if concern_type is None:
            return error_response(
                message="Concern type not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        concern_type.delete()
        return success_response(message="Concern type deleted successfully.")
