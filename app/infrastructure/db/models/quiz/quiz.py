import uuid
import typing
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    registry,
)
from sqlalchemy import (
    Enum as EnumType,
    ForeignKey,
    UUID,
)

from app.core.quiz.entity import (
    QuizType,
    QuestionType,
    QuestionEntity,
    AnsOptionEntity,
    QuizEntity,
)
from ..base import Base
from ..mixin import TimestampMixin

if typing.TYPE_CHECKING:
    from .user import User


class Quiz(Base, TimestampMixin):
    __tablename__ = "quiz"
    name: Mapped[str]
    img: Mapped[str | None] = mapped_column()
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    type: Mapped[EnumType] = mapped_column(
        EnumType(QuizType), default=QuizType.TEST
    )

    author: Mapped["User"] = relationship("User", back_populates="quizzes")
    questions: Mapped[list["Question"]] = relationship(
        "Question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Quiz(id={self.id},\
                name={self.name},\
                questions={self.questions},\
                author_id={self.author_id})"

    def __str__(self) -> str:
        return f"{self.name} by {self.author.username}. \
                {len(self.questions)} questions. Type: {self.type.name}"


class Question(Base, TimestampMixin):
    __tablename__ = "question"

    quiz_id: Mapped[UUID] = mapped_column(
        ForeignKey("quiz.id", ondelete="CASCADE")
    )
    name: Mapped[str]
    img: Mapped[str | None] = mapped_column()
    file: Mapped[str | None] = mapped_column()
    type: Mapped[EnumType] = mapped_column(
        EnumType(QuestionType), default=QuestionType.SINGLE
    )
    correct_count: Mapped[int] = mapped_column(default=0)
    options = relationship("AnsOption", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Question(id={self.id},\
                quiz_id={self.quiz_id},\
                question={self.question},\
                solution={self.solution})"

    def __str__(self) -> str:
        return f"Question in {self.name}."


class AnsOption(Base, TimestampMixin):
    __tablename__ = "ans_option"

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )
    name: Mapped[str]
    img: Mapped[str | None] = mapped_column()
    file: Mapped[str | None] = mapped_column()
    is_correct: Mapped[bool] = mapped_column()

    def __repr__(self):
        return f"AnsOption(id={self.id},\
                question_id={self.question_id},\
                name={self.name},\
                is_correct={self.is_correct})"

    def __str__(self) -> str:
        return f"Answer option for {self.name}."


def map_quiz_tables(mapper_registry: registry):
    quiz_table = Quiz.__table__
    question_table = Question.__table__
    ans_option_table = AnsOption.__table__

    mapper_registry.map_imperatively(
        QuizEntity,
        quiz_table,
        properties={
            "questions": relationship(
                QuestionEntity,
                cascade="all, delete-orphan",
            ),
        },
    )
    mapper_registry.map_imperatively(
        QuestionEntity,
        question_table,
        properties={
            "options": relationship(
                AnsOptionEntity,
                cascade="all, delete-orphan",
                lazy="selectin",
            )
        },
    )
    mapper_registry.map_imperatively(AnsOptionEntity, ans_option_table)
