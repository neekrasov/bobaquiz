from uuid import UUID
from dataclasses import dataclass

from app.shared import Command
from app.core.quiz import dto


@dataclass
class PatchQuizCommand(Command):
    quiz_id: UUID
    quiz: dto.Quiz
