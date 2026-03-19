from rest_framework.views import APIView
from rest_framework import status

from apps.utils.responses import success_response, error_response
from apps.utils.permissions import IsAdmin, IsAdminOrDeveloper
from .models import System
from .serializers import SystemReadSerializer, SystemWriteSerializer


class SystemListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]

    def get(self, request):
        systems = System.objects.select_related('office').all()
        serializer = SystemReadSerializer(systems, many=True)
        return success_response(
            message='Systems retrieved successfully.',
            data=serializer.data
        )

    def post(self, request):
        serializer = SystemWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation error.',
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        system = serializer.save()
        return success_response(
            message='System created successfully.',
            data=SystemReadSerializer(system).data,
            status_code=status.HTTP_201_CREATED
        )


class SystemDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]

    def get_object(self, ulid):
        try:
            return System.objects.select_related('office').get(ulid=ulid)
        except System.DoesNotExist:
            return None

    def get(self, request, ulid):
        system = self.get_object(ulid)
        if system is None:
            return error_response(
                message='System not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = SystemReadSerializer(system)
        return success_response(
            message='System retrieved successfully.',
            data=serializer.data
        )

    def put(self, request, ulid):
        system = self.get_object(ulid)
        if system is None:
            return error_response(
                message='System not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = SystemWriteSerializer(system, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation error.',
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        system = serializer.save()
        return success_response(
            message='System updated successfully.',
            data=SystemReadSerializer(system).data
        )

    def patch(self, request, ulid):
        system = self.get_object(ulid)
        if system is None:
            return error_response(
                message='System not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = SystemWriteSerializer(system, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message='Validation error.',
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        system = serializer.save()
        return success_response(
            message='System updated successfully.',
            data=SystemReadSerializer(system).data
        )

    def delete(self, request, ulid):
        system = self.get_object(ulid)
        if system is None:
            return error_response(
                message='System not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        system.delete()
        return success_response(message='System deleted successfully.')