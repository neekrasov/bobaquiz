from app.shared import DTO
from app.core.quiz.entity import QuestionType
from .ans_option import AnsOption


class Question(DTO):
    name: str
    img: str | None
    file: str | None
    type: QuestionType
    options: list[AnsOption] | None
