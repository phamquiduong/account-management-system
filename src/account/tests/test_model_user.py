import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

TEST_CASES = {
    "email": "test_user@mail.com",
    "password": "Test@1234",
}


@pytest.mark.django_db
def test_create_normal_user():
    user = User.objects.create_user(email=TEST_CASES["email"], password=TEST_CASES["password"])

    assert user.id is not None
    assert user.email == TEST_CASES["email"]
    assert user.check_password(raw_password=TEST_CASES["password"]) is True

    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False

    assert str(user) == f"User: {TEST_CASES['email']}"


@pytest.mark.django_db
def test_create_super_user():
    user = User.objects.create_superuser(email=TEST_CASES["email"], password=TEST_CASES["password"])

    assert user.id is not None
    assert user.email == TEST_CASES["email"]
    assert user.check_password(raw_password=TEST_CASES["password"]) is True

    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True
