from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from src import schemas
from src.models import UserProfile
from src.api import deps
from src.utils import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=schemas.JsonMsg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: UserProfile = Depends(deps.get_current_active_user),
) -> Any:
    """
    Test emails.
    """
    # TODO disallow users from accessing endpoint, only for testing
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
