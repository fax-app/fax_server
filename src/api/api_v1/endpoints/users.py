from typing import Any

from fastapi import APIRouter, Depends, HTTPException


from src import crud, schemas
from src.api import deps
from src.models import UserProfile
from src.core.config import settings
from src.utils import send_new_account_email

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Any = Depends(deps.get_db),
    user_create: schemas.UserCreate,
    current_user: UserProfile = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user. Must Be logged in first.
    """
    user = crud.user.get_by_username(db, username=user_create.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email_to=user.email,
            username=user_create.username,
            password=user_create.password,
        )
    return user.to_dict()


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Any = Depends(deps.get_db),
    user_update: schemas.UserUpdate,
    current_user: UserProfile = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_update)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Any = Depends(deps.get_db),
    current_user: UserProfile = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user.to_dict()


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *, db: Any = Depends(deps.get_db), user_create: schemas.UserCreate
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_username(db, username=user_create.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email_to=user.email,
            username=user_create.username,
            password=user_create.password,
        )
    return user.to_dict()
