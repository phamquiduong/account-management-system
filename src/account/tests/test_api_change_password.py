from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from common.tests.login import login_test

User = get_user_model()

CHANGE_PASSWORD_URL = "/account/api/change-password"


@dataclass
class ChangePasswordTestCase:
    email: str
    password: str
    new_password: str


TEST_CASES: dict[str, ChangePasswordTestCase] = {
    "success": ChangePasswordTestCase(email="user@mail.com", password="Test@1234", new_password="NewTest@1234"),
    "wrong_password": ChangePasswordTestCase(email="user@mail.com", password="Test@1234", new_password="NewTest@1234"),
}


def test_change_password_url():
    assert reverse("account_api_change-password") == CHANGE_PASSWORD_URL


@pytest.mark.django_db
def test_change_password_success():
    client = APIClient()

    login_response = login_test(client, TEST_CASES["success"].email, TEST_CASES["success"].password)

    response = client.patch(
        CHANGE_PASSWORD_URL,
        {
            "old_password": TEST_CASES["success"].password,
            "new_password": TEST_CASES["success"].new_password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check password change success
    login_response.user.refresh_from_db()
    assert login_response.user.check_password(TEST_CASES["success"].new_password) is True

    # Check logout of all devices
    assert BlacklistedToken.objects.filter(token__jti=login_response.jti).exists() is True


@pytest.mark.django_db
def test_change_password_wrong_old_password():
    client = APIClient()

    login_test(client, TEST_CASES["wrong_password"].email, TEST_CASES["wrong_password"].password)

    response = client.patch(
        CHANGE_PASSWORD_URL,
        {
            "old_password": f"{TEST_CASES['wrong_password'].password}+wrong",
            "new_password": TEST_CASES["wrong_password"].new_password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check error
    assert response.data["old_password"] == ["Old password is incorrect."]
