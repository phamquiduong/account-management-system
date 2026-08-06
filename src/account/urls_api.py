from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views.auth_user import AuthUserAPIView
from account.views.change_password import ChangePasswordView
from account.views.user import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="account_api_users")

urlpatterns = [
    path("", include(router.urls)),
    path("users/me", AuthUserAPIView.as_view(), name="account_api_auth_user"),
    path("users/me/change-password", ChangePasswordView.as_view(), name="account_api_change-password"),
]
