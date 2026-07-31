from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.fields.password import PasswordField

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = User
        fields = "id", "email", "password"
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data: dict[str, str]) -> User:
        if User.objects.exists():
            return User.objects.create_user(**validated_data)
        else:
            return User.objects.create_superuser(**validated_data)
