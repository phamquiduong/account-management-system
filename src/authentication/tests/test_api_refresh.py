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
def test_refresh_token_success():
    User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])

    refresh_url = reverse("auth_api_refresh")
    assert refresh_url == "/auth/api/refresh"

    client = APIClient()

    login_res = client.post(
        reverse("auth_api_login"),
        {
            "email": TEST_CASES["email"],
            "password": TEST_CASES["password"],
        },
        format="json",
    )

    old_refresh = login_res.data["refresh"]

    old_payload = jwt.decode(old_refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    old_jti = old_payload["jti"]

    refresh_res = client.post(
        refresh_url,
        {
            "refresh": old_refresh,
        },
        format="json",
    )

    assert refresh_res.status_code == status.HTTP_200_OK

    new_access = refresh_res.data["access"]
    new_refresh = refresh_res.data["refresh"]

    assert new_access is not None
    assert new_refresh is not None

    new_payload = jwt.decode(new_refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    new_jti = new_payload["jti"]

    old_outstanding = OutstandingToken.objects.get(jti=old_jti)
    assert BlacklistedToken.objects.filter(token=old_outstanding).exists() is True

    new_outstanding = OutstandingToken.objects.get(jti=new_jti)
    assert new_outstanding is not None

    assert new_jti != old_jti
