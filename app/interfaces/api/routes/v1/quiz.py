from uuid import UUID
from fastapi import Depends, APIRouter, status, HTTPException

from app.core.quiz.dto.quiz import Quiz
from app.infrastructure.mediator import Mediator
from app.infrastructure.db.models.user import User
from app.core.quiz.usecases.create_quiz.commands import CreateQuizCommand
from app.core.quiz.usecases.read_quiz import QuizServiceReader
from app.core.quiz.usecases.patch_quiz.commands import PatchQuizCommand
from app.core.quiz.usecases.delete_quiz.commands import DeleteQuizCommand
from app.core.quiz.exceptions import QuizNotFoundException

from ...di.stubs import (
    provide_mediator_stub,
    provide_current_user_stub,
    provide_read_quiz_service_stub,
)


router = APIRouter(
    prefix="/quiz",
)


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_quiz(
    quiz: Quiz,
    user: User = Depends(provide_current_user_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    await mediator.send_command(
        CreateQuizCommand(author_id=user.id, quiz=quiz)
    )


@router.get(path="", status_code=status.HTTP_200_OK, response_model=Quiz)
async def read_quiz(
    quiz_id: UUID,
    read_quiz_service: QuizServiceReader = Depends(
        provide_read_quiz_service_stub
    ),
):
    quiz = await read_quiz_service.get_quiz_by_id(quiz_id=quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    return quiz


@router.patch(
    path="",
    response_model=Quiz,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
async def patch_quiz(
    quiz_id: UUID,
    quiz: Quiz,
    mediator: Mediator = Depends(provide_mediator_stub),
):
    await mediator.send_command(
        PatchQuizCommand(
            quiz_id=quiz_id,
            quiz=quiz,
        )
    )


@router.get(
    path="/my",
    status_code=status.HTTP_200_OK,
    response_model=list[Quiz]
)
async def get_my_quizzes(
    user: User = Depends(provide_current_user_stub),
    read_quiz_service: QuizServiceReader = Depends(
        provide_read_quiz_service_stub
    ),
):
    return await read_quiz_service.get_user_quizzes(user_id=user.id)


@router.delete(
    path="/{quiz_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_quiz(
    quiz_id: UUID,
    user: User = Depends(provide_current_user_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    try:
        await mediator.send_command(
            DeleteQuizCommand(
                author_id=user.id,
                quiz_id=quiz_id,
            )
        )
    except QuizNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
