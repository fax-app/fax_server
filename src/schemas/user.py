from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    pass


class UserLogin(UserBase):
    username: str
    password: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserInDBBase(UserBase):
    PK: Optional[str] = None
    SK: Optional[str] = None


# Additional properties to return via API
class User(UserInDBBase):
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    email: EmailStr
    created_at: datetime
    last_login: datetime
    is_active: Optional[bool] = None
    profile_picture_url: Optional[str] = None


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
