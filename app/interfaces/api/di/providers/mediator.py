from fastapi import Depends

from .db import get_dao
from app.infrastructure.db.dao import (
    QuizDAOImpl,
    QuizDAOReaderImpl,
)
from app.infrastructure.mediator import MediatorImpl
from app.core.quiz.usecases.create_quiz.commands import CreateQuizCommand
from app.core.quiz.usecases.create_quiz.handlers import (
    CreateQuizCommandHandler,
)
from app.core.quiz.usecases.patch_quiz.commands import PatchQuizCommand
from app.core.quiz.usecases.patch_quiz.handlers import (
    PatchQuizCommandHandler,
)

from app.core.quiz.usecases.delete_quiz.commands import DeleteQuizCommand
from app.core.quiz.usecases.delete_quiz.handlers import (
    DeleteQuizCommandHandler,
)


def provide_mediator(
    quiz_dao=Depends(get_dao(QuizDAOImpl)),
    quiz_dao_reader=Depends(get_dao(QuizDAOReaderImpl)),
):
    mediator = MediatorImpl()

    mediator.bind_command(
        command_type=CreateQuizCommand,
        handler_type=lambda mediator: CreateQuizCommandHandler(
            mediator=mediator,
            quiz_dao=quiz_dao
        ),
    )

    mediator.bind_command(
        command_type=PatchQuizCommand,
        handler_type=lambda mediator: PatchQuizCommandHandler(
            mediator=mediator,
            quiz_dao=quiz_dao,
            quiz_dao_reader=quiz_dao_reader,
        ),
    )

    mediator.bind_command(
        command_type=DeleteQuizCommand,
        handler_type=lambda mediator: DeleteQuizCommandHandler(
            mediator=mediator,
            quiz_dao=quiz_dao,
            quiz_dao_reader=quiz_dao_reader,
        ),
    )

    return mediator
