from uuid import UUID
from typing import Sequence
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from app.core.solution.entity import QuizSolutionEntity
from app.core.solution.protocols.dao import (
    QuizSolutionDAO,
    QuizSolutionDAOReader,
)
from ..dao.base import BaseDAO, BaseDAOReader


class QuizSolutionDAOImpl(QuizSolutionDAO, BaseDAO):
    async def add_quiz_solution(
        self, solution: QuizSolutionEntity
    ) -> QuizSolutionEntity:
        solution.created_at = QuizSolutionEntity.generate_timestamp()
        self._session.add(solution)
        return solution


class QuizSolutionDAOReaderImpl(QuizSolutionDAOReader, BaseDAOReader):
    async def get_user_solutions(
        self, solution_id: UUID
    ) -> Sequence[QuizSolutionEntity]:
        stmt = (
            select(QuizSolutionEntity)
            .filter_by(user_id=solution_id)
            .options(
                selectinload(QuizSolutionEntity.questions)  # type: ignore
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
