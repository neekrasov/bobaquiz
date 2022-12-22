from typing import Sequence
from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select, delete
from sqlalchemy.engine import Result

from app.infrastructure.db.dao.base import BaseDAO, BaseDAOReader
from app.core.quiz.protocols.dao import QuizDAO, QuizDAOReader
from app.core.quiz.entity import (
    QuizEntity,
)
from app.core.quiz import dto


class QuizDAOImpl(QuizDAO, BaseDAO):
    async def add_quiz(self, quiz: QuizEntity) -> QuizEntity:
        quiz.created_at = QuizEntity.generate_timestamp()
        self._session.add(quiz)
        return quiz

    async def update_quiz(
        self,
        quiz: QuizEntity,
        update_schema: dto.Quiz,
    ) -> QuizEntity:
        """on clarification"""
        raise NotImplementedError

    async def delete_quiz(self, quiz_id, user_id):
        stmt = delete(QuizEntity).where(
            QuizEntity.id == quiz_id and QuizEntity.author_id == user_id
        )
        await self._session.execute(stmt)
        await self._session.commit()


class QuizDAOReaderImpl(QuizDAOReader, BaseDAOReader):
    async def _get(self, **kwargs) -> Result[tuple[QuizEntity]]:
        stmt = (
            select(QuizEntity)
            .filter_by(**kwargs)
            .options(selectinload(QuizEntity.questions))  # type: ignore
        )
        result = await self._session.execute(stmt)
        return result

    async def get_quiz_by_id(self, quiz_id: UUID) -> QuizEntity | None:
        result = await self._get(id=quiz_id)
        quiz = result.scalars().first()
        return quiz

    async def get_user_quizzes(self, user_id: UUID) -> Sequence[QuizEntity]:
        result = await self._get(author_id=user_id)
        quizzes = result.scalars().all()
        return quizzes
