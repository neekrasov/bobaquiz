from sqlalchemy.orm import scoped_session
from passlib.context import CryptContext
from app.settings import Settings
from app.infrastructure.db.models import User


def create_superuser_if_not_exists(
    session: scoped_session,
    settings: Settings
):
    user = (
        session.query(User)
        .filter(
            User.email == settings.superuser_email,
        )
        .first()
    )

    if user:
        return

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    session.add(
        User(
            username=settings.superuser_name,
            email=settings.superuser_email,
            hashed_password=context.hash(settings.superuser_password),
            is_superuser=True,
        )
    )
    session.commit()
