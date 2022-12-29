import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Entity:
    id: uuid.UUID

    @classmethod
    def generate_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    def dict(self) -> dict:
        return asdict(self)


@dataclass
class CreatedTimeStampMixin:
    created_at: datetime = field(init=False)

    @classmethod
    def generate_timestamp(cls) -> datetime:
        return datetime.now()
