from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_verified_email": {"read_only": True},
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
        }
