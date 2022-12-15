import uuid
from enum import Enum
from dataclasses import dataclass, field

from app.shared.entity import Entity
from .question import QuestionEntity


class QuizType(Enum):
    SURVEY = "survey"
    TEST = "test"


@dataclass
class QuizEntity(Entity):
    name: str
    img: str | None
    author_id: uuid.UUID
    type: QuizType
    questions: list[QuestionEntity] = field(default_factory=list)
