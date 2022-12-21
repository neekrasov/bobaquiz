from fastapi import Depends

from app.infrastructure.db.dao.quiz import QuizDAOReaderImpl, QuizDAOReader
from app.core.quiz.usecases.read_quiz import QuizServiceReader
from app.core.solution.protocols.dao import QuizSolutionDAOReader
from app.core.solution.usecase.read_solution import QuizSolutionServiceReader
from app.infrastructure.db.dao.solution import QuizSolutionDAOReaderImpl

from .db import get_dao


def provide_read_quiz_service(
    quiz_dao: QuizDAOReader = Depends(get_dao(QuizDAOReaderImpl)),
) -> QuizServiceReader:
    return QuizServiceReader(quiz_dao_reader=quiz_dao)


def provide_quiz_solution_service(
    quiz_solution_dao: QuizSolutionDAOReader = Depends(
        get_dao(QuizSolutionDAOReaderImpl)
    ),
) -> QuizSolutionServiceReader:
    return QuizSolutionServiceReader(
        quiz_solution_dao_reader=quiz_solution_dao
    )
