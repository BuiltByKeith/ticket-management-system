from rest_framework import serializers
from .models import ConcernType


class ConcernTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcernType
        fields = ["id", "name"]
        read_only_fields = ["ulid"]
