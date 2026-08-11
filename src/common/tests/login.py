from dataclasses import dataclass

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@dataclass
class LoginResponse:
    access: str
    refresh: str
    jti: str
    user: User  # type:ignore


def login_test(client, email: str = "", password: str = "", is_admin: bool = False) -> LoginResponse:
    """
    Function login support test.

    Args:
        client (rest_framework.test.APIClient): The test client
        email (str): Email of test user. If not set email
        password (str): Password of test user. If not set password
        is_admin (bool): Additional information support create user instance

    Returns:
        LoginResponse: Include `access` (access token), `refresh` (refresh token), `jti` (refresh token jti), `user` (the user instance)
    """

    if is_admin is True:
        user = User.objects.create_superuser(email=email, password=password)  # type:ignore

    if is_admin is False:
        user = User.objects.create_user(email=email, password=password)  # type:ignore

    response = client.post(reverse("auth-api-login"), {"email": email, "password": password}, format="json")

    access = response.data["access"]
    refresh = response.data["refresh"]

    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    jti = payload["jti"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    return LoginResponse(access=access, refresh=refresh, jti=jti, user=user)
