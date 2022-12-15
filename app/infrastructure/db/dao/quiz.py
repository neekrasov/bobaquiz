from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.dao.base import BaseDAO
from app.core.quiz.protocols.dao import QuizDAO
from app.core.quiz.entity.quiz import QuizEntity


class QuizDAOImpl(QuizDAO, BaseDAO):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_quiz(self, quiz: QuizEntity) -> QuizEntity:
        self._session.add(quiz)
        return quiz
