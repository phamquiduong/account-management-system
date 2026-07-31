from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

REGISTER_URL = "/account/api/register"


@dataclass
class RegisterTestCase:
    email: str
    password: str


TEST_CASES: dict[str, RegisterTestCase] = {
    "first_user": RegisterTestCase(email="first_user@mail.com", password="Test@1234"),
    "second_user": RegisterTestCase(email="second_user@mail.com", password="Test@1234"),
    "user_short_password": RegisterTestCase(email="user_short_password@mail.com", password="short"),
    "register_conflict": RegisterTestCase(email="register_conflict@mail.com", password="Test@1234"),
}


def test_register_url():
    assert reverse("account_api_register") == REGISTER_URL


@pytest.mark.django_db
def test_register_success():
    client = APIClient()

    response = client.post(
        REGISTER_URL,
        {
            "email": TEST_CASES["first_user"].email,
            "password": TEST_CASES["first_user"].password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_201_CREATED

    # Check id and email in response
    assert "id" in response.data
    assert response.data["email"] == TEST_CASES["first_user"].email

    # Check first user is superuser
    first_user = User.objects.get(id=response.data["id"])
    assert first_user.is_active is True
    assert first_user.is_staff is True
    assert first_user.is_superuser is True

    response = client.post(
        REGISTER_URL,
        {
            "email": TEST_CASES["second_user"].email,
            "password": TEST_CASES["second_user"].password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_201_CREATED

    # Check id and email in response
    assert "id" in response.data
    assert response.data["email"] == TEST_CASES["second_user"].email

    # Check first user is normal user
    second_user = User.objects.get(id=response.data["id"])
    assert second_user.is_active is True
    assert second_user.is_staff is False
    assert second_user.is_superuser is False


@pytest.mark.django_db
def test_password_short():
    client = APIClient()

    response = client.post(
        REGISTER_URL,
        {
            "email": TEST_CASES["user_short_password"].email,
            "password": TEST_CASES["user_short_password"].password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check error message
    assert response.data["password"] == ["This password is too short. It must contain at least 8 characters."]


@pytest.mark.django_db
def test_register_conflict():
    client = APIClient()

    response = client.post(
        REGISTER_URL,
        {
            "email": TEST_CASES["register_conflict"].email,
            "password": TEST_CASES["register_conflict"].password,
        },
        format="json",
    )

    # Check first time register success
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        REGISTER_URL,
        {
            "email": TEST_CASES["register_conflict"].email,
            "password": TEST_CASES["register_conflict"].password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check error message
    assert response.data["email"] == ["user with this email address already exists."]
