from typing import Protocol
from .mediator import Mediator


class Event(Protocol):
    ...


class EventHandler(Protocol):

    def __init__(self, mediator: Mediator):
        ...

    def execute(self, event: Event):
        ...
