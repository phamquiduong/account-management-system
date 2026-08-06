from django.urls import include, path

from account.views.change_password import ChangePasswordView
from account.views.register import RegisterAPIView
from account.views.update_user import UpdateUserView

api_router = [
    path("", UpdateUserView.as_view(), name="account_api_update"),
    path("register", RegisterAPIView.as_view(), name="account_api_register"),
    path("change-password", ChangePasswordView.as_view(), name="account_api_change-password"),
]

urlpatterns = [
    path("api/", include(api_router)),
]
