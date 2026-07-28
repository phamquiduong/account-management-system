import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

TEST_CASES = {
    "email": "test_user@mail.com",
    "password": "Test@1234",
}


@pytest.mark.django_db
def test_login_success():
    login_url = reverse("auth_api_login")
    assert login_url == "/auth/api/login"

    user = User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])
    assert user.last_login is None

    client = APIClient()
    response = client.post(
        login_url,
        {
            "email": TEST_CASES["email"],
            "password": TEST_CASES["password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

    user.refresh_from_db()
    assert user.last_login is not None
