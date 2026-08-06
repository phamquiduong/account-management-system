from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.serializers.auth_user import AuthUserSerializer

User = get_user_model()


@extend_schema(tags=["Authenticated User"])
class AuthUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
