from dataclasses import dataclass

import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from common.tests.login import login_test

User = get_user_model()

REFRESH_URL = "/auth/api/refresh"


@dataclass
class RefreshTestCase:
    email: str
    password: str


TEST_CASES: dict[str, RefreshTestCase] = {
    "normal": RefreshTestCase(email="user@mail.com", password="Test@1234"),
}


def test_refresh_url():
    assert reverse("auth_api_refresh") == REFRESH_URL


@pytest.mark.django_db
def test_refresh_token_success():
    client = APIClient()

    login_response = login_test(client, email=TEST_CASES["normal"].email, password=TEST_CASES["normal"].password)

    refresh_res = client.post(
        REFRESH_URL,
        {
            "refresh": login_response.refresh,
        },
        format="json",
    )

    # Check status
    assert refresh_res.status_code == status.HTTP_200_OK

    # Check access token
    assert "access" in refresh_res.data

    # Check refresh token
    assert "refresh" in refresh_res.data

    # Check revoke old token
    assert BlacklistedToken.objects.filter(token__jti=login_response.jti).exists() is True

    refresh_token = refresh_res.data["refresh"]
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])

    new_outstanding = OutstandingToken.objects.get(jti=payload["jti"])

    # Check save new refresh token
    assert new_outstanding is not None

    # Check not return old token
    assert payload["jti"] != login_response.jti
