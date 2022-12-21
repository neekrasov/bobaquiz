from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass, field

from app.shared import Entity, CreatedTimeStampMixin
from .question import QuestionSolutionEntity


@dataclass
class QuizSolutionEntity(Entity, CreatedTimeStampMixin):
    quiz_id: UUID
    user_id: UUID
    grade: Decimal
    questions: list[QuestionSolutionEntity] = field(default_factory=list)
