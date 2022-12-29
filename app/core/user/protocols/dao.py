from uuid import UUID
from typing import Protocol, Sequence
from datetime import timedelta

from app.shared import DAOReader, DAO
from ..entities.user import UserEntity, Email


class UserDAOReader(DAOReader, Protocol):
    async def get_user_by_email(self, email: Email) -> UserEntity | None:
        ...

    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        ...

    async def get_users_completed_quiz(
        self, quiz_id: UUID
    ) -> Sequence[UserEntity]:
        ...

    async def check_author_quiz(
        self, quiz_id: UUID, author_id: UUID
    ) -> bool:
        ...


class UserDAO(DAO, Protocol):
    async def add_user(self, user: UserEntity) -> UserEntity:
        ...


class AuthDAO(Protocol):
    async def save_refresh_token(
        self, token: str, session_id: str, refresh_token_expire: timedelta
    ) -> None:
        ...

    async def delete_token_if_exists(self, session_id: str) -> None:
        ...
