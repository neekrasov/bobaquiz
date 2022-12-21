from uuid import UUID
from fastapi import Depends, APIRouter, status, HTTPException

from app.core.quiz import dto
from app.infrastructure.mediator import Mediator
from app.infrastructure.db.models import User
from app.core.quiz.exceptions import (
    QuizNotFoundException,
    QuestionNotFoundException,
    AnsOptionNotFoundException,
)
from app.core.quiz.usecases.create_quiz.commands import CreateQuizCommand
from app.core.quiz.usecases.read_quiz import QuizServiceReader
from app.core.quiz.usecases.patch_quiz.commands import PatchQuizCommand
from app.core.quiz.usecases.delete_quiz.commands import DeleteQuizCommand
from app.core.quiz.usecases.answer_quiz.commands import (
    ValidateQuizSolutionCommand,
)

from app.core.solution.usecase.read_solution import QuizSolutionServiceReader

from ..request_models.solution import QuizSolutionRequest
from ..response_models.solution import QuizSolutionResponse
from ..response_models.quiz import QuizResponse


from ...di.stubs import (
    provide_mediator_stub,
    provide_current_user_stub,
    provide_read_quiz_service_stub,
    provide_quiz_solution_service_stub,
)


router = APIRouter(
    prefix="/quiz",
)


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_quiz(
    quiz: dto.Quiz,
    user: User = Depends(provide_current_user_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    await mediator.send_command(
        CreateQuizCommand(author_id=user.id, quiz=quiz)
    )
    return {"message": "Quiz created"}


@router.get(
    path="", status_code=status.HTTP_200_OK, response_model=QuizResponse
)
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
    response_model=dto.Quiz,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
async def patch_quiz(
    quiz_id: UUID,
    quiz: dto.Quiz,
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
    response_model=list[QuizResponse],
    response_model_exclude_none=True,
)
async def get_my_quizzes(
    user: User = Depends(provide_current_user_stub),
    read_quiz_service: QuizServiceReader = Depends(
        provide_read_quiz_service_stub
    ),
):
    quizzes = await read_quiz_service.get_user_quizzes(user_id=user.id)

    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quizzes not found",
        )
    return quizzes


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
    return {"message": "Quiz deleted"}


@router.post(
    path="/send-solution",
    status_code=status.HTTP_201_CREATED,
)
async def send_quiz_solution(
    solution: QuizSolutionRequest,
    user: User = Depends(provide_current_user_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    try:
        await mediator.send_command(
            ValidateQuizSolutionCommand(
                user_id=user.id, solution=dto.QuizSolution(**solution.dict())
            )
        )
    except QuizNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id - {e.args[0]} not found",
        )
    except QuestionNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id - {e.args[0]} not found",
        )
    except AnsOptionNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Answer with id - {e.args[0]} option not found",
        )
    return {"message": "Ok"}


@router.get(
    path="/my-solutions",
    status_code=status.HTTP_200_OK,
    response_model=list[QuizSolutionResponse],
)
async def get_my_solutions(
    user: User = Depends(provide_current_user_stub),
    read_quiz_service: QuizSolutionServiceReader = Depends(
        provide_quiz_solution_service_stub
    ),
):
    solutions = await read_quiz_service.get_user_solutions(user_id=user.id)
    if not solutions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solutions not found",
        )
    return solutions
