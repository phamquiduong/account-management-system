import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

User = get_user_model()

CHANGE_PASSWORD_URL = "/account/api/change-password"


TEST_CASES: dict[str, str] = {
    "email": "user@mail.com",
    "password": "Test@1234",
    "new_password": "NewTest@1234",
}


def test_register_url():
    assert reverse("account_api_change-password") == CHANGE_PASSWORD_URL


@pytest.mark.django_db
def test_change_password_success():
    client = APIClient()

    user = User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])

    response = client.post(
        reverse("auth_api_login"),
        {
            "email": TEST_CASES["email"],
            "password": TEST_CASES["password"],
        },
        format="json",
    )
    refresh = response.data["refresh"]
    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    jti = payload["jti"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    response = client.patch(
        CHANGE_PASSWORD_URL,
        {
            "old_password": TEST_CASES["password"],
            "new_password": TEST_CASES["new_password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.check_password(TEST_CASES["new_password"]) is True

    assert BlacklistedToken.objects.filter(token__jti=jti).exists() is True


@pytest.mark.django_db
def test_change_password_wrong_old_password():
    client = APIClient()

    user = User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])
    client.force_authenticate(user=user)

    response = client.patch(
        CHANGE_PASSWORD_URL,
        {
            "old_password": f"{TEST_CASES['password']}+wrong",
            "new_password": TEST_CASES["new_password"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["old_password"] == ["Old password is incorrect."]
