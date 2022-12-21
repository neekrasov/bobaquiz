import uuid
from enum import Enum
from dataclasses import dataclass, field

from app.shared import Entity
from .ans_option import AnsOptionEntity


class QuestionType(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    NOTHING = "nothing"


@dataclass
class QuestionEntity(Entity):
    quiz_id: uuid.UUID
    name: str
    img: str | None
    file: str | None
    type: QuestionType
    correct_count: int
    options: list[AnsOptionEntity] = field(default_factory=list)

    def get_option(self, option_id: uuid.UUID) -> AnsOptionEntity | None:
        for option in self.options:
            if option.id == option_id:
                return option
        return None
