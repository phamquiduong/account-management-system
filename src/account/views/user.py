from datetime import timedelta
from http import HTTPMethod

from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from account.constants.email import EMAIL_VERIFY_SUBJECT
from account.serializers.register import UserRegisterSerializer
from account.serializers.user import UserSerializer
from mail.services.send_mail import SendMailService

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

    def perform_create(self, serializer):
        user = serializer.save()

        content = SendMailService.render_content(
            "mail/verify_email.html",
            username=user.name or user.email,
            otp="123456",
            otp_expires_at=timezone.now() + timedelta(days=1),
        )
        SendMailService(to=[user.email], subject=EMAIL_VERIFY_SUBJECT, content=content).send()
