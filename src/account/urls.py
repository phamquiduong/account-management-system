from django.urls import include, path

from account.views.register import RegisterAPIView

api_router = [
    path("register", RegisterAPIView.as_view(), name="account_api_register"),
]

urlpatterns = [
    path("api/", include(api_router)),
]
