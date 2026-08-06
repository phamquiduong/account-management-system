from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.tests.login import login_test

User = get_user_model()

UPDATE_USER_URL = "/account/api/"


@dataclass
class UpdateUserTestCase:
    email: str
    name: str


TEST_CASES: dict[str, UpdateUserTestCase] = {
    "success": UpdateUserTestCase(email="user@mail.com", name="User Name"),
}


def test_change_password_url():
    assert reverse("account_api_update") == UPDATE_USER_URL


@pytest.mark.django_db
def test_change_password_success():
    client = APIClient()

    login_response = login_test(client, email=f"register_{TEST_CASES['success'].email}", password="Test@123")

    assert login_response.user.email != TEST_CASES["success"].email
    assert login_response.user.name != TEST_CASES["success"].name

    response = client.patch(
        UPDATE_USER_URL,
        {
            "email": TEST_CASES["success"].email,
            "name": TEST_CASES["success"].name,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check password change success
    login_response.user.refresh_from_db()
    assert login_response.user.email != TEST_CASES["success"].email
    assert login_response.user.name != TEST_CASES["success"].name
