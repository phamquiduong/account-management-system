import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

User = get_user_model()

TEST_CASES = {
    "email": "test@mail.com",
    "password": "Test@1234",
}


@pytest.mark.django_db
def test_logout_success_and_blacklist():
    User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])

    client = APIClient()

    login_url = reverse("auth_api_login")
    logout_url = reverse("auth_api_logout")

    assert logout_url == "/auth/api/logout"

    login_res = client.post(
        login_url,
        {
            "email": TEST_CASES["email"],
            "password": TEST_CASES["password"],
        },
        format="json",
    )

    refresh = login_res.data["refresh"]

    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    jti = payload["jti"]

    logout_res = client.post(
        logout_url,
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert logout_res.status_code == status.HTTP_200_OK

    outstanding = OutstandingToken.objects.get(jti=jti)
    assert outstanding is not None

    assert BlacklistedToken.objects.filter(token=outstanding).exists() is True
