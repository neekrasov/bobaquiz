from enum import Enum
from .base import Base
from sqlalchemy import Enum as EnumType
from sqlalchemy.orm import mapped_column, Mapped, relationship


class SubscriptionLevel(Enum):
    FREE = "free"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    policy: Mapped[bool] = mapped_column(default=True)
    avatar: Mapped[str] = mapped_column(default="")
    sub_id: Mapped[EnumType] = mapped_column(
        EnumType(SubscriptionLevel), default=SubscriptionLevel.FREE
    )
    
    quizzes: Mapped["Quiz"] = relationship("Quiz", back_populates="author") #type: ignore
    quiz_rezults: Mapped[list["QuizResult"]] = relationship("QuizResult", back_populates="user") #type: ignore

    def __repr__(self):
        return f"User(id={self.id},\
                username={self.username},\
                email={self.email},\
                is_active={self.is_active},\
                is_superuser={self.is_superuser},\
                is_staff={self.is_staff},\
                policy={self.policy},\
                avatar={self.avatar},\
                sub_id={self.sub_id})"
