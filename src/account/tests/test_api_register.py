from typing import TypedDict

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

REGISTER_URL = "/account/api/register"


class UserCase(TypedDict):
    email: str
    password: str


TEST_CASES: dict[str, UserCase] = {
    "first_user": {
        "email": "first_user@mail.com",
        "password": "Test@1234",
    },
    "second_user": {
        "email": "second_user@mail.com",
        "password": "Test@1234",
    },
    "user_short_password": {
        "email": "user_short_password@mail.com",
        "password": "short",
    },
}


def test_register_url():
    assert reverse("account_api_register") == REGISTER_URL


@pytest.mark.django_db
def test_register_success():
    client = APIClient()

    # Test create the first user. User will be super admin
    first_user_test_case = TEST_CASES["first_user"]
    response = client.post(
        REGISTER_URL,
        {
            "email": first_user_test_case["email"],
            "password": first_user_test_case["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert "id" in response.data
    assert "email" in response.data
    assert response.data["email"] == first_user_test_case["email"]

    first_user = User.objects.get(id=response.data["id"])
    assert first_user.is_active is True
    assert first_user.is_staff is True
    assert first_user.is_superuser is True

    # Test create the second user. User will be normal
    second_user_test_case = TEST_CASES["second_user"]
    response = client.post(
        REGISTER_URL,
        {
            "email": second_user_test_case["email"],
            "password": second_user_test_case["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert "id" in response.data
    assert "email" in response.data
    assert response.data["email"] == second_user_test_case["email"]

    second_user = User.objects.get(id=response.data["id"])
    assert second_user.is_active is True
    assert second_user.is_staff is False
    assert second_user.is_superuser is False


@pytest.mark.django_db
def test_password_short():
    client = APIClient()

    user_test_case = TEST_CASES["user_short_password"]
    response = client.post(
        REGISTER_URL,
        {
            "email": user_test_case["email"],
            "password": user_test_case["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["password"] == ["This password is too short. It must contain at least 8 characters."]


@pytest.mark.django_db
def test_register_conflict():
    client = APIClient()

    user_test_case = TEST_CASES["first_user"]
    response = client.post(
        REGISTER_URL,
        {
            "email": user_test_case["email"],
            "password": user_test_case["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        REGISTER_URL,
        {
            "email": user_test_case["email"],
            "password": user_test_case["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"] == ["user with this email address already exists."]
