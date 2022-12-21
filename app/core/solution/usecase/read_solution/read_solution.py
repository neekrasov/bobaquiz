from typing import Sequence
from uuid import UUID
from ...entity import QuizSolutionEntity
from ...protocols.dao import QuizSolutionDAOReader


class QuizSolutionServiceReader:
    def __init__(self, quiz_solution_dao_reader: QuizSolutionDAOReader):
        self._quiz_solution_dao_reader = quiz_solution_dao_reader

    async def get_user_solutions(
        self, user_id: UUID
    ) -> Sequence[QuizSolutionEntity]:
        return await self._quiz_solution_dao_reader.get_user_solutions(user_id)
