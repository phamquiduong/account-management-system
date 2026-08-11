from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from common.tests.login import login_test

User = get_user_model()


@dataclass
class LogoutTestCase:
    email: str
    password: str


TEST_CASES: dict[str, LogoutTestCase] = {
    "normal": LogoutTestCase(email="user@mail.com", password="Test@1234"),
}


@pytest.mark.django_db
def test_logout_success_and_blacklist():
    client = APIClient()

    login_response = login_test(client, email=TEST_CASES["normal"].email, password=TEST_CASES["normal"].password)

    response = client.post(
        reverse("auth-api-logout"),
        {
            "refresh": login_response.refresh,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check revoke token
    assert BlacklistedToken.objects.filter(token__jti=login_response.jti).exists() is True
