from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    Enum as EnumType,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    registry,
)

from app.core.user.entities.user import (
    SubscriptionLevelEnum,
    UserEntity,
    SubscriptionLevelEntity,
)
from ..base import Base
from ..mixin import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str]
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    policy: Mapped[bool] = mapped_column(default=True)
    sub_id: Mapped[EnumType] = mapped_column(
        ForeignKey("subscription_level.id", ondelete="CASCADE")
    )

    subscription: Mapped["SubscriptionLevel"] = relationship(
        "SubscriptionLevel",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self):
        return f"User(id={self.id},\
                username={self.username},\
                email={self.email},\
                is_active={self.is_active},\
                is_superuser={self.is_superuser},\
                is_staff={self.is_staff},\
                policy={self.policy},\
                avatar={self.avatar},\
                subscription={self.sub_id})"

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


class SubscriptionLevel(Base):
    __tablename__ = "subscription_level"

    type: Mapped[SubscriptionLevelEnum] = mapped_column(
        EnumType(SubscriptionLevelEnum), primary_key=True
    )
    valid_from: Mapped[datetime | None] = mapped_column(default=None)
    valid_until: Mapped[datetime | None] = mapped_column(default=None)
    user: Mapped[User] = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"SubscriptionLevel(type={self.type},\
                valid_from={self.valid_from},\
                valid_until={self.valid_until})"


def map_user_tables(mapper_registry: registry):
    user_table = User.__table__
    subscription_level_table = SubscriptionLevel.__table__

    mapper_registry.map_imperatively(
        UserEntity,
        user_table,
        properties={
            "subscription": relationship(
                SubscriptionLevelEntity,
                uselist=False,
                cascade="all, delete-orphan",
                single_parent=True,
            )
        },
    )
    mapper_registry.map_imperatively(
        SubscriptionLevelEntity, subscription_level_table
    )
