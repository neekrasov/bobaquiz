from datetime import datetime
from sqlalchemy.orm import declarative_mixin, mapped_column, Mapped


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
