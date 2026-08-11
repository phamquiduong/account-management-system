from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.tests.login import login_test

User = get_user_model()


@dataclass
class UpdateAuthUserTestCase:
    email: str
    name: str


TEST_CASES: dict[str, UpdateAuthUserTestCase] = {
    "success": UpdateAuthUserTestCase(email="user@mail.com", name="User Name"),
}


@pytest.mark.django_db
def test_update_auth_user_success():
    client = APIClient()

    login_response = login_test(client, email=f"register_{TEST_CASES['success'].email}", password="Test@123")

    assert login_response.user.email != TEST_CASES["success"].email
    assert login_response.user.name != TEST_CASES["success"].name
    assert login_response.user.is_active is True

    response = client.patch(
        reverse("account-api-auth_user"),
        {
            "email": TEST_CASES["success"].email,
            "name": TEST_CASES["success"].name,
            "is_active": False,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check update auth user success
    login_response.user.refresh_from_db()
    assert login_response.user.email == TEST_CASES["success"].email
    assert login_response.user.name == TEST_CASES["success"].name
    assert login_response.user.is_active is False
