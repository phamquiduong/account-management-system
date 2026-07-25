from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "id", "email", "password"
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data: dict[str, str]) -> User:
        if User.objects.exists():
            return User.objects.create_user(**validated_data)  # type:ignore
        else:
            return User.objects.create_superuser(**validated_data)  # type:ignore
