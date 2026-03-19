from rest_framework.views import APIView
from rest_framework import status

from apps.utils.responses import success_response, error_response
from apps.utils.permissions import IsAdmin, IsAdminOrDeveloper
from .models import Office
from .serializers import OfficeSerializer


class OfficeListCreateView(APIView):
    """
    GET /api/v1/offices/        - list of all offices (admin and developer access)
    POST /api/v1/offices        - create and office(admin only)
    """

    def get_permissions(self):
        """
        Dynamically assign permissions based on the HTTP method.
        Get is accessible by both roles, POST is admin only.
        """

        if self.request.method == "GET":
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]

    def get(self, request):
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return success_response(
            message="Offices retrieved successfully!", data=serializer.data
        )

    def post(self, request):
        serializer = OfficeSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Office created successfully!",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class OfficeDetailView(APIView):
    """
    GET /api/v1/offices/<ulid>/     -retrieve a single office
    PUT /api/v1/office/<ulid>/      -update an office (admin only)
    DELETE /api/v1/offices/<ulid>/  -delete an office (admin only)
    """

    # Dynamic permission handler
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrDeveloper()]
        return [IsAdmin()]

    # function to find the office using the ULID. Scans the entire DB with the same requested ULID and return that ID unless it found nothing and returns None
    def get_object(self, ulid):
        """
        Helper method to fetch the office by ulid.
        Returns None if not found so the view can return 404.
        """

        try:
            return Office.objects.get(ulid=ulid)
        except Office.DoesNotExist:
            return None

    # Get a specific office by ULID which was already processed at the get_object helper method above
    def get(self, request, ulid):
        office = self.get_object(ulid)
        if office is None:
            return error_response(
                message="Office not found", status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = OfficeSerializer(office)
        return success_response(
            message="Office retrieved successfully!", data=serializer.data
        )

    def put(self, request, ulid):
        office = self.get_object(ulid)
        if office is None:
            return error_response(
                message="Office not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        # partial=False means ALL required fields must be provided
        serializer = OfficeSerializer(office, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Office updated successfully!", data=serializer.data
        )

    def patch(self, request, ulid):
        office = self.get_object(ulid)
        if office is None:
            return error_response(
                message="Office not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        # partial=True means only the provided fields are updated
        serializer = OfficeSerializer(office, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return success_response(
            message="Office updated successfully.", data=serializer.data
        )

    def delete(self, request, ulid):
        office = self.get_object(ulid)
        if office is None:
            return error_response(
                message="Office not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        office.delete()
        return success_response(
            message="Office deleted successfully.", status_code=status.HTTP_200_OK
        )
