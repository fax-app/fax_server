from typing import Dict, Any

from fastapi.testclient import TestClient

from src import crud
from src.core.config import settings
from src.models import UserProfile
from src.schemas.user import UserCreate, UserUpdate
from src.tests.utils.utils import random_email, random_lower_string, random_username


def create_test_user(db: Any) -> UserProfile:
    user = crud.user.get_by_username(db, username=settings.TEST_USER)
    if not user:
        user_create = UserCreate(
            username=settings.TEST_USER,
            password=settings.TEST_USER_PASSWORD,
            email=settings.TEST_USER_EMAIL,
        )
        user = crud.user.create(db, obj_in=user_create)

    return user


def get_test_user_token_headers(client: TestClient) -> Dict[str, str]:
    return user_token_headers(
        client=client, username=settings.TEST_USER, password=settings.TEST_USER_PASSWORD
    )


def user_token_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    login_data = {
        "username": username,
        "password": password,
    }

    response = client.post(
        f"{settings.API_PREFIX_STR}/login/access-token", data=login_data
    )
    tokens = response.json()
    auth_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(
    db: Any, password: str = None, is_active: bool = None
) -> UserProfile:
    username = random_username()
    email = random_email()
    if password is None:
        password = random_lower_string()
    if is_active is None:
        is_active = True
    user_create = UserCreate(
        username=username, email=email, password=password, is_active=is_active
    )
    user = crud.user.create(db=db, obj_in=user_create)
    return user


def authentication_token_from_username(
    *, client: TestClient, username: str, db: Any
) -> Dict[str, str]:
    """
    Return a valid token for the user with given username.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    email = random_email()
    user = crud.user.get_by_username(db, username=username)
    if not user:
        user_create = UserCreate(username=username, email=email, password=password)
        user = crud.user.create(db, obj_in=user_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_token_headers(client=client, username=username, password=password)
