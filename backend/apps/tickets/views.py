from rest_framework.views import APIView
from rest_framework import status

from apps.utils.responses import success_response, error_response
from apps.utils.permissions import IsAdmin, IsAdminOrDeveloper
from .models import Ticket
from .serializers import (
    TicketReadSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
    TicketTrackingSerializer,
)


class TicketListCreateView(APIView):
    """
    GET  /api/v1/tickets/   — list all tickets (admin and developer)
    POST /api/v1/tickets/   — submit a ticket (public)
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return []  # Public — no authentication required
        return [IsAdminOrDeveloper()]

    def get(self, request):
        tickets = Ticket.objects.select_related(
            'system', 'concern_type', 'assigned_to', 'system__office'
        ).all()
        serializer = TicketReadSerializer(tickets, many=True)
        return success_response(
            message='Tickets retrieved successfully.',
            data=serializer.data
        )

    def post(self, request):
        serializer = TicketCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation error.',
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        ticket = serializer.save()
        return success_response(
            message='Ticket submitted successfully.',
            data={
                'reference_id': ticket.reference_id,
                'tracking_password': ticket.tracking_password,
                'ulid': ticket.ulid,
            },
            status_code=status.HTTP_201_CREATED
        )


class TicketDetailView(APIView):
    """
    GET   /api/v1/tickets/<ulid>/   — retrieve a ticket (admin and developer)
    PATCH /api/v1/tickets/<ulid>/   — update status/priority/assignment (admin and developer)
    """
    permission_classes = [IsAdminOrDeveloper]

    def get_object(self, ulid):
        try:
            return Ticket.objects.select_related(
                'system', 'concern_type', 'assigned_to', 'system__office'
            ).get(ulid=ulid)
        except Ticket.DoesNotExist:
            return None

    def get(self, request, ulid):
        ticket = self.get_object(ulid)
        if ticket is None:
            return error_response(
                message='Ticket not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = TicketReadSerializer(ticket)
        return success_response(
            message='Ticket retrieved successfully.',
            data=serializer.data
        )

    def patch(self, request, ulid):
        ticket = self.get_object(ulid)
        if ticket is None:
            return error_response(
                message='Ticket not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = TicketUpdateSerializer(ticket, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message='Validation error.',
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        ticket = serializer.save()
        return success_response(
            message='Ticket updated successfully.',
            data=TicketReadSerializer(ticket).data
        )


class TicketTrackingView(APIView):
    """
    POST /api/v1/tickets/track/
    Public endpoint for requesters to track their ticket status.
    Requires reference_id and tracking_password.
    """
    permission_classes = []  # fully public

    def post(self, request):
        reference_id = request.data.get('reference_id')
        tracking_password = request.data.get('tracking_password')

        if not reference_id or not tracking_password:
            return error_response(
                message='Both reference_id and tracking_password are required.',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            ticket = Ticket.objects.select_related(
                'system', 'concern_type', 'system__office'
            ).get(reference_id=reference_id, tracking_password=tracking_password)
        except Ticket.DoesNotExist:
            return error_response(
                message='Invalid reference ID or tracking password.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = TicketTrackingSerializer(ticket)
        return success_response(
            message='Ticket retrieved successfully.',
            data=serializer.data
        )