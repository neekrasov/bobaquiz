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
    is_verified: Mapped[bool] = mapped_column(default=False)
    policy: Mapped[bool] = mapped_column(default=True)
    avatar: Mapped[str] = mapped_column(default="")
    sub_id: Mapped[EnumType] = mapped_column(
        EnumType(SubscriptionLevel), default=SubscriptionLevel.FREE
    )

    quizzes: Mapped["Quiz"] = relationship("Quiz", back_populates="author", cascade="all, delete-orphan")  # type: ignore
    quiz_rezults: Mapped[list["QuizResult"]] = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")  # type: ignore

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

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
