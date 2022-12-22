from uuid import UUID
from fastapi_users import schemas, BaseUserManager, UUIDIDMixin
from app.infrastructure.db.models.user import User
from app.core.user.entity.enum import SubscriptionLevel


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):  # type: ignore
    pass


class UserRead(schemas.BaseUser[UUID]):
    username: str
    policy: bool
    avatar: str
    sub_id: SubscriptionLevel | None


class UserCreate(schemas.BaseUserCreate):
    username: str
    policy: bool
    sub_id: SubscriptionLevel


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    policy: bool
    sub_id: SubscriptionLevel