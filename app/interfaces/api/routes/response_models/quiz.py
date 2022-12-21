from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.core.quiz import dto


class IDScheme(BaseModel):
    id: UUID


class AnsOptionResponse(dto.AnsOption, IDScheme):
    pass


class QuestionResponse(dto.Question, IDScheme):
    correct_count: int
    options: list[AnsOptionResponse] | None  # type: ignore


class QuizResponse(dto.Quiz, IDScheme):
    questions: list[QuestionResponse] | None  # type: ignore
    created_at: datetime
