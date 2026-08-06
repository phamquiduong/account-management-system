from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from account.serializers.register import UserRegisterSerializer
from account.serializers.user import UserSerializer

User = get_user_model()


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["is_superuser", "is_staff", "is_active"]
    search_fields = ["email", "name"]

    def get_permissions(self):
        if self.request.method in [HTTPMethod.PUT, HTTPMethod.PATCH, HTTPMethod.DELETE]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == HTTPMethod.POST:
            return UserRegisterSerializer
        return super().get_serializer_class()
