import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import JSON, ForeignKey
from .base import Base, uuidpk
from .user import User


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[uuidpk]
    name: Mapped[str]
    ans_options: Mapped[str] = mapped_column(JSON, default={})
    img: Mapped[str] = mapped_column(default="")
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship("User", back_populates="quizzes")
    results: Mapped["QuizResult"] = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Quiz(id={self.id},\
                name={self.name},\
                ans_options={self.ans_options},\
                author_id={self.author_id})"


class QuizResult(Base):
    __tablename__ = "quiz_result"
    quiz_id: Mapped[uuidpk] = mapped_column(ForeignKey("quiz.id", ondelete="CASCADE"))
    user_id: Mapped[uuidpk] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    result: Mapped[str] = mapped_column(JSON, default={})

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="results")
    user: Mapped["User"] = relationship("User", back_populates="quiz_rezults")

    def __repr__(self):
        return f"QuizResult(id={self.id},\
                quiz_id={self.quiz_id},\
                user_id={self.user_id},\
                result={self.result})"
