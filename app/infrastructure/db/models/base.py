import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, registry
from sqlalchemy import UUID, TIMESTAMP
from typing_extensions import Annotated

uuidpk = Annotated[
    uuid.UUID,
    UUID(as_uuid=True),
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True),
]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            datetime: TIMESTAMP(timezone=True),
            uuid.UUID: UUID(as_uuid=True),
        }
    )

    id: Mapped[uuidpk]
