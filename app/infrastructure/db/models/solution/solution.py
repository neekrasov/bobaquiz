from decimal import Decimal
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    registry,
)

from app.core.solution.entity import (
    AnsOptionSolutionEntity,
    QuestionSolutionEntity,
    QuizSolutionEntity,
)

from ..base import Base
from ..mixin import TimestampMixin


class AnsOptionSolution(Base):
    __tablename__ = "ans_option_solution"
    ans_option_id: Mapped[UUID] = mapped_column(ForeignKey("ans_option.id"))
    question_solution_id: Mapped[UUID] = mapped_column(
        ForeignKey("question_solution.id")
    )
    is_correct: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"AnswerSolution(id={self.id},\
                answer_id={self.answer_id},\
                question_solution_id={self.question_solution_id},\
                solution={self.solution},\
                is_correct={self.is_correct})"

    def __str__(self) -> str:
        return f"AnswerSolution for answer {self.ans_option_id}."


class QuestionSolution(Base):
    __tablename__ = "question_solution"
    question_id: Mapped[UUID] = mapped_column(ForeignKey("question.id"))
    quiz_solution_id: Mapped[UUID] = mapped_column(
        ForeignKey("quiz_solution.id")
    )
    grade: Mapped[Decimal] = mapped_column(NUMERIC(), default=0.0)

    options = relationship(
        "AnsOptionSolution", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f"QuestionSolution(id={self.id},\
                question_id={self.question_id},\
                quiz_solution_id={self.quiz_solution_id},\
                grade={self.grade})"

    def __str__(self) -> str:
        return f"QuestionSolution for question {self.question_id}."


class QuizSolution(Base, TimestampMixin):
    __tablename__ = "quiz_solution"
    quiz_id: Mapped[UUID] = mapped_column(ForeignKey("quiz.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    grade: Mapped[Decimal] = mapped_column(NUMERIC(), default=0.0)

    questions = relationship("QuestionSolution", cascade="all, delete-orphan")

    def __repr__(self):
        return f"QuizSolution(id={self.id},\
                quiz_id={self.quiz_id},\
                user_id={self.user_id},\
                grade={self.grade})"

    def __str__(self) -> str:
        return f"QuizSolution for quiz {self.quiz_id}."


def map_solution_tables(mapper_registry: registry):
    ans_option_solution_table = AnsOptionSolution.__table__
    question_solution_table = QuestionSolution.__table__
    quiz_solution_table = QuizSolution.__table__

    mapper_registry.map_imperatively(
        AnsOptionSolutionEntity,
        ans_option_solution_table,
    )

    mapper_registry.map_imperatively(
        QuestionSolutionEntity,
        question_solution_table,
        properties={
            "options": relationship(
                AnsOptionSolutionEntity,
                cascade="all, delete-orphan",
                lazy="selectin",
            )
        },
    )

    mapper_registry.map_imperatively(
        QuizSolutionEntity,
        quiz_solution_table,
        properties={
            "questions": relationship(
                QuestionSolutionEntity,
                cascade="all, delete-orphan",
            )
        },
    )
