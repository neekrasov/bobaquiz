from dataclasses import dataclass
from app.shared import Command
from ...dto.user import UserCreate


@dataclass
class CreateUserCommand(Command):
    user: UserCreate
