from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.tests.login import login_test
from common.tests.permission import require_admin_permission_test

User = get_user_model()


@dataclass
class AdminUpdateUserTestCase:
    email: str
    name: str


TEST_CASES: dict[str, AdminUpdateUserTestCase] = {
    "success": AdminUpdateUserTestCase(email="user@mail.com", name="User Name"),
}


@pytest.mark.django_db
def test_update_user_success():
    client = APIClient()

    user = User.objects.create_user(  # type:ignore
        email=f"register_{TEST_CASES['success'].email}",
        name=f"Register {TEST_CASES['success'].name}",
        password="Test@123",
    )

    # Check user before update
    assert user.email != TEST_CASES["success"].email
    assert user.name != TEST_CASES["success"].name
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_staff is False

    login_test(client, email="admin@mail.com", password="Test@123", is_admin=True)
    response = client.patch(
        reverse("account-api-users-detail", kwargs={"pk": user.id}),
        {
            "email": TEST_CASES["success"].email,
            "name": TEST_CASES["success"].name,
            "is_active": False,
            "is_superuser": True,
            "is_staff": True,
        },
        format="json",
    )

    # Check status
    assert response.status_code == status.HTTP_200_OK

    # Check admin update user success
    user.refresh_from_db()
    assert user.email == TEST_CASES["success"].email
    assert user.name == TEST_CASES["success"].name
    assert user.is_active is False
    assert user.is_superuser is True
    assert user.is_staff is True


@pytest.mark.django_db
def test_update_user_not_have_permission():
    user = User.objects.create_user(email="update_user@mail.com", password="Test@123")  # type:ignore
    require_admin_permission_test(url=reverse("account-api-users-detail", kwargs={"pk": user.id}))
