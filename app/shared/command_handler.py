from typing import Protocol

from .mediator import Mediator


class Command(Protocol):
    ...


class CommandHandler(Protocol):
    def __init__(self, mediator: Mediator):
        ...

    async def execute(self, command) -> None:
        ...
