from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.core.settings import Settings
from src.db.models import User


def create_superuser_if_not_exists(session: Session, settings: Settings):
    user = (
        session.query(User)
        .filter(
            User.email == settings.superuser_email,
        )
        .first()
    )

    if user:
        print("Superuser already exists")
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
