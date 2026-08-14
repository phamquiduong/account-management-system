from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.fields.password import PasswordField

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_verified_email": {"read_only": True},
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
        }

    def create(self, validated_data: dict[str, str]) -> User:
        if User.objects.exists():
            return User.objects.create_user(**validated_data)
        else:
            return User.objects.create_superuser(**validated_data)
