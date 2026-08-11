from rest_framework import status
from rest_framework.test import APIClient

from common.tests.login import login_test


def require_admin_permission_test(url: str) -> None:
    """
    Require admin permission test.

    Args:
        url (str): Test the normal user can not access this url
    """
    client = APIClient()

    login_test(client, email="normal_user@mail.com", password="Test@123")
    response = client.patch(url, {}, format="json")

    # Check status
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check error response
    assert response.data["detail"] == "You do not have permission to perform this action."
