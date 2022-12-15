from uuid import UUID
from dataclasses import dataclass

from app.shared import Command
from app.core.quiz.dto.quiz import QuizCreate


@dataclass
class CreateQuizCommand(Command):
    author_id: UUID
    quiz: QuizCreate
