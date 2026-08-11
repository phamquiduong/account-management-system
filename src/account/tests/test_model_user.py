from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass
class UserModelTestCase:
    email: str
    password: str


TEST_CASES: dict[str, UserModelTestCase] = {
    "normal": UserModelTestCase(email="user@mail.com", password="Test@1234"),
}


@pytest.mark.django_db
def test_create_normal_user():
    user = User.objects.create_user(email=TEST_CASES["normal"].email, password=TEST_CASES["normal"].password)  # type:ignore

    # Check can create user
    assert user.id is not None

    # Check email
    assert user.email == TEST_CASES["normal"].email

    # Check password
    assert user.check_password(raw_password=TEST_CASES["normal"].password) is True

    # Check account is active
    assert user.is_active is True

    # Check not super user
    assert user.is_staff is False
    assert user.is_superuser is False

    assert str(user) == f"User: {TEST_CASES['normal'].email}"


@pytest.mark.django_db
def test_create_super_user():
    user = User.objects.create_superuser(email=TEST_CASES["normal"].email, password=TEST_CASES["normal"].password)  # type:ignore

    # Check can create user
    assert user.id is not None

    # Check email
    assert user.email == TEST_CASES["normal"].email

    # Check password
    assert user.check_password(raw_password=TEST_CASES["normal"].password) is True

    # Check account is active
    assert user.is_active is True

    # Check not super user
    assert user.is_staff is True
    assert user.is_superuser is True
