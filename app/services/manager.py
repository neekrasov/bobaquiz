from uuid import UUID
from fastapi_users import BaseUserManager, UUIDIDMixin
from app.infrastructure.db.models.user import User


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):  # type: ignore
    pass