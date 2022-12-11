import uuid
import typing
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Enum as EnumType, JSON

from .base import Base, uuidpk
from .mixin import TimestampMixin
from ..enums.quiz import QuizType, QuestionType

if typing.TYPE_CHECKING:
    from .user import User


class Quiz(Base, TimestampMixin):
    __tablename__ = "quiz"

    id: Mapped[uuidpk]
    name: Mapped[str]
    img: Mapped[str | None] = mapped_column()
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    type: Mapped[EnumType] = mapped_column(
        EnumType(QuizType), default=QuizType.TEST
    )

    author: Mapped["User"] = relationship("User", back_populates="quizzes")
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    results: Mapped[list["QuizResult"]] = relationship(
        "QuizResult", back_populates="quiz", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Quiz(id={self.id},\
                name={self.name},\
                questions={self.questions},\
                author_id={self.author_id})"

    def __str__(self) -> str:
        return f"{self.name} by {self.author.username}. \
                {len(self.questions)} questions. Type: {self.type.name}"


class QuizResult(Base, TimestampMixin):
    __tablename__ = "quiz_result"

    quiz_id: Mapped[uuidpk] = mapped_column(ForeignKey("quiz.id"), unique=True)
    user_id: Mapped[uuidpk] = mapped_column(
        ForeignKey("users.id"), unique=True
    )
    question_id: Mapped[uuidpk] = mapped_column(
        ForeignKey("question.id"), unique=True
    )

    solution: Mapped[str | None] = mapped_column(JSON)

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="results")
    user: Mapped["User"] = relationship("User", back_populates="quiz_rezults")

    def __repr__(self):
        return f"QuizResult(id={self.id},\
                quiz_id={self.quiz_id},\
                user_id={self.user_id},\
                question_id={self.question_id},\
                solution={self.solution})"

    def __str__(self) -> str:
        return f"Quiz result for {self.user.username} in {self.quiz.name}."


class Question(Base, TimestampMixin):
    __tablename__ = "question"

    quiz_id: Mapped[uuidpk] = mapped_column(ForeignKey("quiz.id"))
    img: Mapped[str | None] = mapped_column()
    file: Mapped[str | None] = mapped_column()
    type: Mapped[EnumType] = mapped_column(
        EnumType(QuestionType), default=QuestionType.SINGLE
    )

    question: Mapped[str] = mapped_column(JSON, nullable=True)
    solution: Mapped[str] = mapped_column(JSON, nullable=True)

    quiz = relationship("Quiz", back_populates="questions")

    def __repr__(self):
        return f"Question(id={self.id},\
                quiz_id={self.quiz_id},\
                question={self.question},\
                solution={self.solution})"

    def __str__(self) -> str:
        return f"Question in {self.quiz.name}."
