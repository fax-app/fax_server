from typing import Optional, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from src import crud, schemas
from src.models import UserProfile
from src.core import security
from src.core.config import settings
from src.db import table
import json

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX_STR}/login/access-token"
)


def get_db() -> Any:
    return table


def get_current_user(
    db: Any = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Optional[UserProfile]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
        if token_data.sub is not None:
            primary_key = json.loads(token_data.sub.replace("'", '"'))
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_profile = crud.user.get(db, primary_key=primary_key)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")
    user = UserProfile(user_profile)
    return user


def get_current_active_user(
    current_user: UserProfile = Depends(get_current_user),
) -> Optional[UserProfile]:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
