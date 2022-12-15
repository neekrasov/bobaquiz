import uuid
from dataclasses import dataclass


@dataclass
class Entity:
    id: uuid.UUID

    @classmethod
    def generate_id(self) -> uuid.UUID:
        return uuid.uuid4()
