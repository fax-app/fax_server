from typing import Dict, Generator, Any

import pytest
from fastapi.testclient import TestClient

from src.db import table
from src.main import app
from src.models import UserProfile
from src.tests.utils.user import (
    authentication_token_from_username,
    get_test_user_token_headers,
    create_test_user,
)


@pytest.fixture(scope="session")
def db() -> Any:
    return table


@pytest.fixture(autouse=True, scope="session")
def test_user(db: Any) -> UserProfile:
    return create_test_user(db)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user_token_headers(client: TestClient) -> Dict[str, str]:
    return get_test_user_token_headers(client)


@pytest.fixture(scope="module")
def user_token_headers(client: TestClient, db: Any, username: str) -> Dict[str, str]:
    return authentication_token_from_username(client=client, username=username, db=db)
