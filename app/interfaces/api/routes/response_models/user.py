from uuid import UUID
from pydantic import BaseModel, validator

from app.core.user.entities.user import (
    SubscriptionLevelEnum,
)


class UserReadResponse(BaseModel):
    id: UUID
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    policy: bool
    subscription: SubscriptionLevelEnum

    @validator("subscription", pre=True)
    def subscription_level(cls, v):
        return v["type"]


class UsersWithCountResponse(BaseModel):
    users: list[UserReadResponse]
    count: int
