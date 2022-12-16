from app.shared import DTO
from app.core.quiz.entity import QuizType
from .question import Question


class Quiz(DTO):
    name: str
    img: str | None
    type: QuizType
    questions: list[Question] | None
