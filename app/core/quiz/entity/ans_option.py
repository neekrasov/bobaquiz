import uuid
from dataclasses import dataclass

from app.shared.entity import Entity


@dataclass
class AnsOptionEntity(Entity):
    question_id: uuid.UUID
    name: str
    img: str | None
    file: str | None
    is_correct: bool
