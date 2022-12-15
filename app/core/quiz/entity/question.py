import uuid
from enum import Enum
from dataclasses import dataclass, field

from app.shared import Entity
from .ans_option import AnsOptionEntity


class QuestionType(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


@dataclass
class QuestionEntity(Entity):
    quiz_id: uuid.UUID
    name: str
    img: str | None
    file: str | None
    type: QuestionType
    options: list[AnsOptionEntity] = field(default_factory=list)
