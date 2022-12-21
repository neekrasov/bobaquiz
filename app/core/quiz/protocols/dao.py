from typing import Protocol, Sequence
from uuid import UUID
from app.shared.dao import DAO, DAOReader

from app.core.quiz.entity.quiz import QuizEntity
from app.core.quiz import dto


class QuizDAO(DAO, Protocol):
    async def add_quiz(self, quiz: QuizEntity) -> QuizEntity:
        ...

    async def update_quiz(
        self, quiz: QuizEntity, update_schema: dto.Quiz
    ) -> QuizEntity:
        ...

    async def delete_quiz(self, quiz_id: UUID, user_id: UUID) -> None:
        ...


class QuizDAOReader(DAOReader, Protocol):
    async def get_quiz_by_id(self, quiz_id: UUID) -> QuizEntity | None:
        ...

    async def get_user_quizzes(self, user_id: UUID) -> Sequence[QuizEntity]:
        ...
