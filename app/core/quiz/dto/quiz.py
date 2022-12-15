from app.shared import DTO
from app.core.quiz.entity import QuizType
from .question import QuestionCreate


class QuizCreate(DTO):
    name: str
    img: str | None
    type: QuizType
    questions: list[QuestionCreate] | None
