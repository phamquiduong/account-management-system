from django.urls import path

from authentication.views.login import LoginAPIView
from authentication.views.logout import LogoutAPIView
from authentication.views.refresh import RefreshTokenAPIView

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="auth-api-login"),
    path("logout", LogoutAPIView.as_view(), name="auth-api-logout"),
    path("refresh", RefreshTokenAPIView.as_view(), name="auth-api-refresh"),
]
