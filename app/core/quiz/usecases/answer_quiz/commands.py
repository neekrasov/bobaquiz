from uuid import UUID
from dataclasses import dataclass

from app.shared import Command
from ...dto.quiz_answer import QuizSolution


@dataclass
class ValidateQuizSolutionCommand(Command):
    user_id: UUID
    solution: QuizSolution
