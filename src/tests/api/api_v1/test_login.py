from typing import Dict

from fastapi.testclient import TestClient

from src.core.config import settings
from src.utils import generate_password_reset_token


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.TEST_USER,
        "password": settings.TEST_USER_PASSWORD,
    }
    response = client.post(
        f"{settings.API_PREFIX_STR}/login/access-token", data=login_data
    )
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, test_user_token_headers: Dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_PREFIX_STR}/login/test-token",
        headers=test_user_token_headers,
    )
    result = response.json()
    assert response.status_code == 200
    assert "email" in result


def test_password_recovery_email(client: TestClient) -> None:
    username = "test_user"
    response = client.post(f"{settings.API_PREFIX_STR}/password-recovery/{username}")
    assert response.json() == {"msg": "Password recovery email sent"}


def test_reset_password(client: TestClient) -> None:
    username = "test_user"
    token = generate_password_reset_token(username=username)
    payload = {"new_password": "testpass", "token": token}
    response = client.post(f"{settings.API_PREFIX_STR}/reset-password/", json=payload)
    assert response.json() == {"msg": "Password updated successfully"}
