from uuid import UUID
from decimal import Decimal
from app.shared import DTO


class AnsOptionSolution(DTO):
    ans_option_id: UUID
    is_correct: bool | None = None


class QuestionSolution(DTO):
    question_id: UUID
    options: list[AnsOptionSolution]
    grade: Decimal | None = None


class QuizSolution(DTO):
    quiz_id: UUID
    questions: list[QuestionSolution]
    grade: Decimal | None = None
