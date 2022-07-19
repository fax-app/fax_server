from typing import Optional, Any
from datetime import datetime

from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.schemas.user import UserCreate, UserUpdate
from src.models import UserProfile


class CRUDUserProfile(CRUDBase[UserCreate, UserUpdate]):
    def get_by_username(self, db: Any, *, username: str) -> Optional[UserProfile]:
        response = db.get_item(Key={"PK": f"USER#{username}", "SK": "PROFILE"})
        if "Item" not in response:
            return None
        else:
            return UserProfile(response["Item"])

    def create(self, db: Any, *, obj_in: UserCreate) -> UserProfile:
        profile = UserProfile()
        profile.PK = f"USER#{obj_in.username}"
        profile.SK = "PROFILE"
        profile.full_name = f"{obj_in.full_name}"
        profile.hashed_password = f"{get_password_hash(obj_in.password)}"
        profile.email = f"{obj_in.email}"
        profile.created_at = datetime.now().isoformat()
        profile.is_active = True

        db.put_item(Item=profile.to_dict())
        return profile

    # def update(
    #     self, db: Any, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Any, *, username: str, password: str
    ) -> Optional[UserProfile]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    def is_active(self, user: dict) -> bool:
        return user["is_active"]


user = CRUDUserProfile()
