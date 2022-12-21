import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entity:
    id: uuid.UUID

    @classmethod
    def generate_id(cls) -> uuid.UUID:
        return uuid.uuid4()


@dataclass
class CreatedTimeStampMixin:
    created_at: datetime | None

    @classmethod
    def generate_timestamp(cls) -> datetime:
        return datetime.now()
