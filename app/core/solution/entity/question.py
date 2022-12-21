from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass, field

from app.shared import Entity
from .ans_option import AnsOptionSolutionEntity


@dataclass
class QuestionSolutionEntity(Entity):
    question_id: UUID
    quiz_solution_id: UUID
    grade: Decimal
    options: list[AnsOptionSolutionEntity] = field(default_factory=list)
