import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    id: uuid.UUID

    @classmethod
    def generate_id(cls) -> uuid.UUID:
        return uuid.uuid4()


@dataclass
class CreatedTimeStampMixin:
    created_at: datetime = field(init=False)

    @classmethod
    def generate_timestamp(cls) -> datetime:
        return datetime.now()
