from typing import Dict, Any

from fastapi.testclient import TestClient

from src import crud
from src.core.config import settings
from src.tests.utils.utils import random_username, random_lower_string, random_email


def test_get_users_me(
    client: TestClient, test_user_token_headers: Dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_PREFIX_STR}/users/me", headers=test_user_token_headers
    )
    current_user = response.json()
    assert current_user
    assert current_user["PK"] == "USER#test_user"
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_update_user_me(
    client: TestClient, test_user_token_headers: Dict[str, str]
) -> None:
    user_update = {"password": "testpass"}
    response = client.put(
        f"{settings.API_PREFIX_STR}/users/me",
        headers=test_user_token_headers,
        json=user_update,
    )
    current_user = response.json()
    assert current_user
    assert current_user["PK"] == "USER#test_user"
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_create_user_new_username(
    client: TestClient, test_user_token_headers: dict, db: Any
) -> None:
    username = random_username()
    email = random_email()
    password = random_lower_string()
    data = {"username": username, "email": email, "password": password}
    response = client.post(
        f"{settings.API_PREFIX_STR}/users/",
        headers=test_user_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    user = crud.user.get_by_username(db, username=username)
    assert user
    assert user.email == email


def test_create_user_existing_username(
    client: TestClient, test_user_token_headers: dict, db: Any
) -> None:
    username = settings.TEST_USER
    email = random_email()
    password = random_lower_string()
    data = {"username": username, "email": email, "password": password}
    response = client.post(
        f"{settings.API_PREFIX_STR}/users/",
        headers=test_user_token_headers,
        json=data,
    )
    created_user = response.json()
    assert response.status_code == 400
    assert "PK" not in created_user


def test_create_user_open_registration(
    client: TestClient, test_user_token_headers: Dict[str, str]
) -> None:
    username = random_username()
    email = random_email()
    password = random_lower_string()
    data = {"username": username, "email": email, "password": password}
    response = client.post(
        f"{settings.API_PREFIX_STR}/users/open",
        json=data,
    )
    assert response.status_code == 200
    assert "PK" in response.json()
