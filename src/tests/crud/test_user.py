from typing import Any

from src import crud
from src.core.security import verify_password
from src.schemas.user import UserCreate, UserUpdate
from src.tests.utils.utils import random_email, random_lower_string, random_username
from src.tests.utils.user import create_random_user


def test_create_user(db: Any) -> None:
    # code from create_random_user copied for clarity
    username = random_username()
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(username=username, email=email, password=password)
    user = crud.user.create(db, obj_in=user_create)
    crud.user.remove(db, user.primary_key())
    assert user.PK == f"USER#{username}"
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Any) -> None:
    password = random_lower_string()
    user = create_random_user(db, password)
    authenticated_user = crud.user.authenticate(
        db, username=user.username(), password=password
    )
    crud.user.remove(db, user.primary_key())
    if authenticated_user is not None:
        assert user.username() == authenticated_user.username()
    else:
        assert False


def test_not_authenticate_user(db: Any) -> None:
    password = random_lower_string()
    user = create_random_user(db, password)
    password = "wrong password"
    non_authenticated_user = crud.user.authenticate(
        db, username=user.username(), password=password
    )
    crud.user.remove(db, user.primary_key())
    assert non_authenticated_user is None


def test_check_if_user_is_active(db: Any) -> None:
    user = create_random_user(db)
    is_active = crud.user.is_active(user)
    crud.user.remove(db, user.primary_key())
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Any) -> None:
    user = create_random_user(db, is_active=False)
    is_active = crud.user.is_active(user)
    crud.user.remove(db, user.primary_key())
    assert is_active is False


def test_get_user(db: Any) -> None:
    user = create_random_user(db)
    user_from_db = crud.user.get(db, primary_key=user.primary_key())
    crud.user.remove(db, user.primary_key())
    assert user_from_db
    assert user.email == user_from_db["email"]


def test_get_user_by_username(db: Any) -> None:
    user = create_random_user(db)
    user_from_db = crud.user.get_by_username(db, username=user.username())
    crud.user.remove(db, user.primary_key())
    assert user_from_db
    assert user.email == user_from_db.email


def test_update_user(db: Any) -> None:
    user = create_random_user(db)
    new_password = random_lower_string()
    user_create_update = UserUpdate(password=new_password)
    crud.user.update(db, db_obj=user, obj_in=user_create_update)
    user_from_db = crud.user.get(db, primary_key=user.primary_key())
    crud.user.remove(db, user.primary_key())
    assert user_from_db
    assert user.email == user_from_db["email"]
    assert verify_password(new_password, user_from_db["hashed_password"])
