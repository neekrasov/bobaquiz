from typing import Sequence
from uuid import UUID
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload

from .base import BaseDAO, BaseDAOReader
from app.core.user.protocols.dao import UserDAO, UserDAOReader
from app.core.user.entities.user import (
    UserEntity,
    Email,
    QuizSolutionEntityID,
    QuizID,
)


class UserDAOImpl(UserDAO, BaseDAO):
    async def add_user(self, user: UserEntity) -> UserEntity:
        user.created_at = UserEntity.generate_timestamp()
        self._session.add(user)
        return user


class UserDAOReaderImpl(UserDAOReader, BaseDAOReader):
    async def get_user_by_email(self, email: Email) -> UserEntity | None:
        stmt = (
            select(UserEntity)
            .filter_by(email=email)
            .options(selectinload(UserEntity.subscription))  # type: ignore
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        stmt = (
            select(UserEntity)
            .filter_by(id=user_id)
            .options(selectinload(UserEntity.subscription))  # type: ignore
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_users_completed_quiz(
        self, quiz_id: UUID
    ) -> Sequence[UserEntity]:
        stmt = (
            select(UserEntity)
            .join(QuizSolutionEntityID)
            .filter(QuizSolutionEntityID.quiz_id == quiz_id)  # type: ignore
            .options(selectinload(UserEntity.subscription))  # type: ignore
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def check_author_quiz(self, quiz_id, author_id):
        stmt = (
            select(QuizID)
            .filter(QuizID.id == quiz_id)
            .filter(QuizID.author_id == author_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first() is not None
