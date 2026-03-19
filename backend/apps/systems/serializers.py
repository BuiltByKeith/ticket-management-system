from rest_framework import serializers
from .models import System
from apps.offices.models import Office
from apps.offices.serializers import OfficeSerializer


class SystemReadSerializer(serializers.ModelSerializer):
    """
    Used for GET requests.
    Returns nested office data so the client gets full context without making a second request
    """

    office = OfficeSerializer(read_only=True)

    class Meta:
        model = System
        fields = [
            "ulid",
            "name",
            "acronym",
            "office",
            "tech_stack_used",
            "date_created",
            "date_updated",
        ]

        read_only_fields = ["ulid", "date_created", "date_updated"]


class SystemWriteSerializer(serializers.ModelSerializer):
    """
    Userd for POST/PUT/PATCH Requests.
    Accepts office_ulid instead of the internal office id, then resolves it to the actual Office instance
    """

    office_ulid = serializers.CharField(write_only=True)

    class Meta:
        model = System
        fields = [
            "ulid",
            "name",
            "acronym",
            "office_ulid",
            "tech_stack_used",
            "date_created",
            "date_updated",
        ]

        read_only_fields = ["ulid", "date_created", "date_updated"]

    def validate_office_ulid(self, value):
        """
        Checks that the provided office_ulid actually exists.
        Raises a validation error if not found.
        """
        try:
            office = Office.objects.get(ulid=value)
        except Office.DoesNotExist:
            raise serializers.ValidationError("Office with this ULID does not exist.")
        return office

    def create(self, validated_data):
        # validated_data['office_ulid] is now the Office instance
        # after passing through the validate_office_ulid method
        office = validated_data.pop("office_ulid")
        return System.objects.create(office=office, **validated_data)

    def update(self, instance, validated_data):
        office = validated_data.pop("office_ulid", None)
        if office:
            instance.office = office
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
