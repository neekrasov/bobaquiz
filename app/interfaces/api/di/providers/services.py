from fastapi import Depends

from app.infrastructure.db.dao.quiz import QuizDAOReaderImpl, QuizDAOReader
from app.core.quiz.usecases.read_quiz import QuizServiceReader

from .db import get_dao


def provide_read_quiz_service(
    quiz_dao: QuizDAOReader = Depends(get_dao(QuizDAOReaderImpl)),
) -> QuizServiceReader:
    return QuizServiceReader(quiz_dao_reader=quiz_dao)
