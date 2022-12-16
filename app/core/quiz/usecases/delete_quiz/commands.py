from uuid import UUID
from app.shared import Command
from dataclasses import dataclass


@dataclass
class DeleteQuizCommand(Command):
    author_id: UUID
    quiz_id: UUID
