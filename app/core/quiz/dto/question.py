from app.shared import DTO
from app.core.quiz.entity import QuestionType
from .ans_option import AnsOptionCreate


class QuestionCreate(DTO):
    name: str
    img: str | None
    file: str | None
    type: QuestionType
    options: list[AnsOptionCreate] | None
