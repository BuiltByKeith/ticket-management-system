from rest_framework import serializers
from .models import Ticket
from apps.systems.models import System
from apps.concern_types.models import ConcernType
from apps.users.models import User
from apps.systems.serializers import SystemReadSerializer
from apps.concern_types.serializers import ConcernTypeSerializer
from apps.users.serializers import UserMinimalSerializer


class TicketReadSerializer(serializers.ModelSerializer):
    """
    Used for GET requests (admin/developer views).
    Returns full nested data for system, concern type, and assigned_to.
    Excludes tracking_password - that is never returned to internal users.
    """

    system = SystemReadSerializer(read_only=True)
    concern_type = ConcernTypeSerializer(read_only=True)
    assigned_to = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "ulid",
            "reference_id",
            "requester_email",
            "requester_full_name",
            "system",
            "concern_type",
            "description",
            "file_attachment",
            "assigned_to",
            "status",
            "priority",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["ulid", "date_created", "date_updated"]


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Used for the public ticket submission form.
    Accepts ulids for system and concern_type, resolves them to instances.
    reference_id and tracking_password are auto-generated - never accepted as input.
    """

    system_ulid = serializers.CharField(write_only=True)
    concern_type_ulid = serializers.CharField(write_only=True)

    class Meta:
        model = Ticket
        fields = [
            "ulid",
            "reference_id",
            "requester_email",
            "requester_full_name",
            "system_ulid",
            "concern_type_ulid",
            "description",
            "file_attachment",
        ]

        read_only_fields = ["ulid", "reference_id"]

    def validate_system_ulid(self, value):
        try:
            system = System.objects.get(ulid=value)

        except System.DoesNotExist:
            raise serializers.ValidationError("System with this ULID does not exists")
        return system

    def validate_concern_type_ulid(self, value):
        try:
            concern_type = ConcernType.objects.get(ulid=value)
        except ConcernType.DoesNotExist:
            raise serializers.ValidationError(
                "Concern type with this ULID does not exists"
            )
        return concern_type

    def create(self, validated_data):
        system = validated_data.pop("system_ulid")
        concern_type = validated_data.pop("concern_type_ulid")
        return Ticket.objects.create(
            system=system, concern_type=concern_type, **validated_data
        )


class TicketUpdateSerializer(serializers.ModelSerializer):
    """
    Used by admins to assign tickets and update priority.
    Used by developers to update ticket status.
    assigned_to_ulid resolves to a User instance.
    """

    assigned_to_ulid = serializers.CharField(
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Ticket
        fields = ["ulid", "assigned_to_ulid", "status", "priority"]
        read_only_fields = ["ulid"]

    def validate_assigned_to_ulid(self, value):
        if value is None:
            return None
        try:
            user = User.objects.get(ulid=value, role="developer")
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Developer with this ULID does not exist or is not a developer."
            )
        return user

    def update(self, instance, validated_data):
        assigned_to = validated_data.pop("assigned_to_ulid", None)
        if assigned_to is not None:
            instance.assigned_to = assigned_to
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TicketTrackingSerializer(serializers.ModelSerializer):
    """
    Used for the public ticket tracking page.
    Returns limited fields - no internal data like assigned developer details.
    tracking_password is never returned here either.
    """

    system = SystemReadSerializer(read_only=True)
    concern_type = ConcernTypeSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "reference_id",
            "requester_email",
            "requester_full_name",
            "system",
            "concern_type",
            "description",
            "status",
            "priority",
            "date_created",
            "date_updated",
        ]
