from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserReadSerializer(serializers.ModelSerializer):
    """
    Used for GET requests.
    Never exposes id or password
    """

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "ulid",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "position",
            "role",
            "is_active",
            "date_created",
            "date_updated",
        ]

        read_only_fields = ["ulid", "date_created", "date_updated"]


class UserWriteSerializer(serializers.ModelSerializer):
    """
    Used for POST/PUT/PATCH requests (admin creating/updating users).
    Password is write-only and gets hashed before saving.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "ulid",
            "email",
            "first_name",
            "last_name",
            "position",
            "role",
            "is_active",
            "password",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["ulid", "date_created", "date_updated"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # Hashes the password - never store plain text
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash the new password if provided
        instance.save()
        return instance


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Used when embedding user infor inside other serializers,
    like showing who a ticket is assigned to.
    Returns only the essential fields to avoid over-fetching.
    """

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["ulid", "full_name", "email", "position", "role"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)