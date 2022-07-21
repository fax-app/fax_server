from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm

from src import crud, schemas
from src.api import deps
from src.core import security
from src.core.config import settings
from src.models import UserProfile
from src.schemas import UserUpdate
from src.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Any = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"PK": user.PK, "SK": user.SK}
    return {
        "access_token": security.create_access_token(
            payload, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: UserProfile = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    print(current_user.to_dict())
    return current_user.to_dict()


@router.post("/password-recovery/{username}", response_model=schemas.JsonMsg)
def recover_password(username: str, db: Any = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_username(db, username=username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(username=username)
    send_reset_password_email(
        email_to=user.email, username=username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.JsonMsg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Any = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    username = verify_password_reset_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_update = UserUpdate(password=new_password)
    crud.user.update(db, db_obj=user, obj_in=user_update)
    return {"msg": "Password updated successfully"}
