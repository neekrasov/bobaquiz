from typing import Protocol


class Mediator(Protocol):
    def bind_command(self, command_type, handler_type):
        ...

    async def send_command(self, command):
        ...

    def bind_event(self, event_type, handler_type):
        ...

    async def publish_event(self, event):
        ...
