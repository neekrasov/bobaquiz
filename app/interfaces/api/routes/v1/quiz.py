from fastapi import Depends, APIRouter, status

from app.core.quiz.dto.quiz import QuizCreate
from app.infrastructure.mediator import Mediator
from app.infrastructure.db.models.user import User
from app.core.quiz.usecases.create_quiz.commands import CreateQuizCommand
from ...di.stubs import (
    provide_mediator_stub,
    provide_current_user_stub,
)


router = APIRouter(
    prefix="/quiz",
)


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_quiz(
    quiz: QuizCreate,
    user: User = Depends(provide_current_user_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    await mediator.send_command(
        CreateQuizCommand(
            author_id=user.id,
            quiz=quiz
        )
    )
