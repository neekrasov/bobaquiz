from fastapi import Depends

from app.infrastructure.mediator import MediatorImpl
from app.core.quiz.usecases.create_quiz.commands import CreateQuizCommand
from app.core.quiz.usecases.create_quiz.handlers import (
    CreateQuizCommandHandler,
)
from app.infrastructure.db.dao import (
    QuizDAOImpl,
)
from .db import get_dao


def provide_mediator(
    quiz_dao=Depends(get_dao(QuizDAOImpl)),
):
    mediator = MediatorImpl()

    mediator.bind_command(
        command_type=CreateQuizCommand,
        handler_type=lambda mediator: CreateQuizCommandHandler(
            mediator=mediator,
            quiz_dao=quiz_dao,
        ),
    )
    return mediator
