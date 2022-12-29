from typing import Protocol
from datetime import timedelta

from app.shared import DAOReader, DAO
from ..entities.user import UserEntity, Email, UserID


class UserDAOReader(DAOReader, Protocol):
    async def get_user_by_email(self, email: Email) -> UserEntity | None:
        ...

    async def get_user_by_id(self, user_id: UserID) -> UserEntity | None:
        ...


class UserDAO(DAO, Protocol):
    async def add_user(self, user: UserEntity) -> UserEntity:
        ...


class AuthDAO(Protocol):
    async def save_refresh_token(
        self,
        token: str,
        session_id: str,
        refresh_token_expire: timedelta
    ) -> None:
        ...

    async def delete_token_if_exists(self, session_id: str) -> None:
        ...
