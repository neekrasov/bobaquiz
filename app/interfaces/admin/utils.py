from sqlalchemy.orm import scoped_session
from passlib.context import CryptContext

from app.core.user.entities import (
    SubscriptionLevelEnum,
)
from app.infrastructure.db.models.user import User, SubscriptionLevel
from app.settings import Settings


def create_superuser_if_not_exists(
    session: scoped_session, settings: Settings
):
    user = (
        session.query(User)
        .filter(
            User.email == settings.superuser_email,  # type: ignore
        )
        .first()
    )

    if user:
        return

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    sub_premium = SubscriptionLevel(
        type=SubscriptionLevelEnum.PREMIUM,
    )

    session.add(
        User(
            username=settings.superuser_name,
            email=settings.superuser_email,
            hashed_password=context.hash(settings.superuser_password),
            is_superuser=True,
            subscription=sub_premium,
        )
    )
    session.commit()
