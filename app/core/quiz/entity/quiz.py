import uuid
from enum import Enum
from dataclasses import dataclass, field

from app.shared.entity import Entity, CreatedTimeStampMixin
from .question import QuestionEntity


class QuizType(Enum):
    SURVEY = "survey"
    TEST = "test"


@dataclass
class QuizEntity(Entity, CreatedTimeStampMixin):
    name: str
    img: str | None
    author_id: uuid.UUID
    type: QuizType
    questions: list[QuestionEntity] = field(default_factory=list)

    def get_question(self, question_id: uuid.UUID) -> QuestionEntity | None:
        for question in self.questions:
            if question.id == question_id:
                return question
        return None
