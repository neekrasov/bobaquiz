from pydantic import BaseModel

from app.core.user.entities.user import (
    SubscriptionLevelEnum,
    UserID,
)


class UserReadResponse(BaseModel):
    id: UserID
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    policy: bool
    subscription: SubscriptionLevelEnum
