from uuid import UUID
from typing import Protocol, Sequence
from app.shared import DAO

from ..entity import QuizSolutionEntity


class QuizSolutionDAO(DAO, Protocol):
    async def add_quiz_solution(
        self, solution: QuizSolutionEntity
    ) -> QuizSolutionEntity:
        ...


class QuizSolutionDAOReader(DAO, Protocol):
    async def get_user_solutions(
        self, user_id: UUID
    ) -> Sequence[QuizSolutionEntity]:
        ...
