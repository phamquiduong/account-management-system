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
    user: User


def login_test(client, email: str, password: str, user: User | None = None) -> LoginResponse:
    if user is None:
        user: User = User.objects.create_user(email=email, password=password)

    response = client.post(reverse("auth_api_login"), {"email": email, "password": password}, format="json")
    access = response.data["access"]
    refresh = response.data["refresh"]

    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
    jti = payload["jti"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    return LoginResponse(access=access, refresh=refresh, jti=jti, user=user)
