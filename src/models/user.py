from .base import BaseDBModel


class UserProfile(BaseDBModel):
    full_name: str | None
    email: str
    hashed_password: str
    is_active: bool
    created_at: str
    last_login: str
    profile_picture_url: str | None

    def __init__(self, attrs: dict = None):
        if attrs is not None:
            super().__init__(attrs)
