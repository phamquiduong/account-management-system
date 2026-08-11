from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@dataclass
class LoginTestCase:
    email: str
    password: str


TEST_CASES: dict[str, LoginTestCase] = {
    "normal": LoginTestCase(email="user@mail.com", password="Test@1234"),
}


@pytest.mark.django_db
def test_login_success():
    user = User.objects.create_user(email=TEST_CASES["normal"].email, password=TEST_CASES["normal"].password)

    # Check user has not login
    assert user.last_login is None

    client = APIClient()
    response = client.post(
        reverse("auth-api-login"),
        {
            "email": TEST_CASES["normal"].email,
            "password": TEST_CASES["normal"].password,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check access token
    assert "access" in response.data

    # Check refresh token
    assert "refresh" in response.data

    user.refresh_from_db()

    # Check save last login data
    assert user.last_login is not None
