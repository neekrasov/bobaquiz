from uuid import UUID
from dataclasses import dataclass

from app.shared import Event

from ...dto.quiz_answer import QuizSolution


@dataclass
class QuizSolutionValidatedEvent(Event):
    user_id: UUID
    solution: QuizSolution
