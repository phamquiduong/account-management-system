from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name")
        extra_kwargs = {
            "id": {"read_only": True},
        }
