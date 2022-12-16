from uuid import UUID
from app.core.quiz.entity.quiz import QuizEntity
from app.core.quiz.protocols.dao import QuizDAOReader


class QuizServiceReader:
    def __init__(self, quiz_dao_reader: QuizDAOReader):
        self._quiz_dao_reader = quiz_dao_reader

    async def get_quiz_by_id(self, quiz_id: UUID) -> QuizEntity | None:
        return await self._quiz_dao_reader.get_quiz_by_id(quiz_id)

    async def get_user_quizzes(self, user_id: UUID) -> list[QuizEntity] | None:
        return await self._quiz_dao_reader.get_user_quizzes(user_id)
