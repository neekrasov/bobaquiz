from uuid import UUID
from dataclasses import dataclass

from app.shared import Entity


@dataclass
class AnsOptionSolutionEntity(Entity):
    ans_option_id: UUID
    question_solution_id: UUID
    is_correct: bool
