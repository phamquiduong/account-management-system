from drf_spectacular.utils import extend_schema
from rest_framework import generics

from account.serializers.register import UserRegisterSerializer


@extend_schema(tags=["Account"])
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
