import uuid
from fastapi_users import schemas

from app.infrastructure.db.models.user import SubscriptionLevel


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    policy: bool
    avatar: str
    sub_id: SubscriptionLevel


class UserCreate(schemas.BaseUserCreate):
    username: str
    policy: bool


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    policy: bool
    sub_id: SubscriptionLevel
