from fastapi import Depends

from app.settings import Settings, get_settings
from app.core.quiz.protocols.dao import QuizDAOReader
from app.core.solution.protocols.dao import QuizSolutionDAOReader
from app.core.user.protocols.dao import UserDAOReader, AuthDAO
from app.infrastructure.db.dao import (
    QuizDAOReaderImpl,
    QuizSolutionDAOReaderImpl,
    UserDAOReaderImpl,
)
from app.core.quiz.usecases.read_quiz import QuizServiceReader
from app.core.solution.usecase.read_solution import QuizSolutionServiceReader
from app.core.user.usecases.read_users import UserReaderService
from app.core.user.usecases.auth import AuthUserService

from .db import get_dao
from ..stubs import (
    provide_user_reader_service_stub,
    provide_auth_dao_stub,
)


def provide_read_quiz_service(
    quiz_dao: QuizDAOReader = Depends(get_dao(QuizDAOReaderImpl)),
) -> QuizServiceReader:
    return QuizServiceReader(quiz_dao_reader=quiz_dao)


def provide_quiz_solution_service(
    quiz_solution_dao_reader: QuizSolutionDAOReader = Depends(
        get_dao(QuizSolutionDAOReaderImpl)
    ),
) -> QuizSolutionServiceReader:
    return QuizSolutionServiceReader(quiz_solution_dao_reader)


def provide_user_reader_service(
    user_reader_dao: UserDAOReader = Depends(get_dao(UserDAOReaderImpl)),
) -> UserReaderService:
    return UserReaderService(user_reader_dao)


def provide_auth_service(
    users_reader_service: UserReaderService = Depends(
        provide_user_reader_service_stub
    ),
    auth_dao: AuthDAO = Depends(provide_auth_dao_stub),
    settings: Settings = Depends(get_settings),
) -> AuthUserService:
    return AuthUserService(
        users_reader_service=users_reader_service,
        auth_dao=auth_dao,
        secret_key=settings.secret_key,
        access_token_expire=settings.access_token_expire,
        refresh_token_expire=settings.refresh_token_expire,
    )
