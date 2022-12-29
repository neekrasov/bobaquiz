from fastapi import Depends

from .db import get_dao
from app.infrastructure.db.dao import (
    QuizDAOImpl,
    QuizDAOReaderImpl,
    UserDAOImpl,
    QuizSolutionDAOImpl,
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

from app.core.quiz.usecases.answer_quiz import (
    QuizSolutionValidatedEvent,
    ValidateQuizSolutionCommand,
    ValidateQuizSolutionCommandHandler,
)

from app.core.solution.usecase.create_solution import (
    QuizSolutionValidatedEventHandler,
)

from app.core.user.usecases.create_user import (
    CreateUserCommand,
    CreateBaseUserCommandHandler,
)


def provide_mediator(
    quiz_dao=Depends(get_dao(QuizDAOImpl)),
    quiz_dao_reader=Depends(get_dao(QuizDAOReaderImpl)),
    quiz_solution_dao=Depends(get_dao(QuizSolutionDAOImpl)),
    user_dao=Depends(get_dao(UserDAOImpl)),
):
    mediator = MediatorImpl()

    mediator.bind_command(
        command_type=CreateQuizCommand,
        handler_type=lambda mediator: CreateQuizCommandHandler(
            mediator=mediator, quiz_dao=quiz_dao
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

    mediator.bind_command(
        command_type=ValidateQuizSolutionCommand,
        handler_type=lambda mediator: ValidateQuizSolutionCommandHandler(
            mediator=mediator,
            quiz_dao_reader=quiz_dao_reader,
        ),
    )

    mediator.bind_event(
        event_type=QuizSolutionValidatedEvent,
        handler_type=lambda mediator: QuizSolutionValidatedEventHandler(
            mediator=mediator,
            quiz_solution_dao=quiz_solution_dao,
        ),
    )

    mediator.bind_command(
        command_type=CreateUserCommand,
        handler_type=lambda mediator: CreateBaseUserCommandHandler(
            mediator=mediator,
            user_dao=user_dao,
        ),
    )

    return mediator
