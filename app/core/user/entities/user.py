import uuid
from typing import NewType
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from app.shared import Entity, CreatedTimeStampMixin

RawPassword = NewType("RawPassword", str)
HashedPassword = NewType("HashedPassword", str)
Username = NewType("Username", str)
Email = NewType("Email", str)


class QuizID(Entity):
    id: uuid.UUID
    author_id: uuid.UUID


class QuizSolutionEntityID(Entity):
    quiz_id: uuid.UUID
    user_id: uuid.UUID


class SubscriptionLevelEnum(Enum):
    FREE = "free"
    PREMIUM = "premium"


@dataclass
class SubscriptionLevelEntity(Entity):
    type: SubscriptionLevelEnum
    valid_from: datetime | None = None
    valid_until: datetime | None = None


@dataclass
class UserEntity(Entity, CreatedTimeStampMixin):
    username: Username
    hashed_password: HashedPassword
    email: Email
    subscription: SubscriptionLevelEntity

    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    is_verified: bool = False
    policy: bool = False

    def __repr__(self):
        return f"User(id={self.id},\
                username={self.username},\
                email={self.email},\
                is_active={self.is_active},\
                is_superuser={self.is_superuser},\
                is_staff={self.is_staff},\
                policy={self.policy},\
                subscription={self.subscription})"
