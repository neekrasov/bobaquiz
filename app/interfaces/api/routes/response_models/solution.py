from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class AnsOptionSolutionResponse(BaseModel):
    ans_option_id: UUID


class QuestionSolutionResponse(BaseModel):
    question_id: UUID
    grade: Decimal
    options: list[AnsOptionSolutionResponse] | None


class QuizSolutionResponse(BaseModel):
    quiz_id: UUID
    grade: Decimal
    questions: list[QuestionSolutionResponse] | None
    created_at: datetime
