from typing import Type, Callable
from app.shared import (
    Mediator,
    CommandHandler,
    Command,
    EventHandler,
    Event,
    EventEmitter,
    Listener,
)


class MediatorImpl(Mediator):
    def __init__(self):
        self._ee = EventEmitterImpl()
        self._commands = {}

    def bind_command(
        self,
        command_type: Type[Command],
        handler_type: Type[CommandHandler],
    ):
        self._commands[command_type] = handler_type

    async def send_command(self, command: Command):
        handler_type = self._commands.get(
            type(command),
        )

        if not handler_type:
            return

        await handler_type(self).execute(command)

    def bind_event(
        self,
        event_type: Type[Event],
        handler_type: Type[EventHandler],
    ):
        self._ee.on(
            event_type,
            lambda event: handler_type(self).execute(event),
        )

    async def publish_event(self, event: Event):
        await self._ee.emit(
            type(event),
            event,
        )

    def __str__(self):
        return f"Mediator \
                \n commands: {self._commands}  \
                \n event_emitter: {self._ee}"


class ListenerImpl(Listener):
    def __init__(self, event: Event, handler: Callable):
        self._event = event
        self._handler = handler

    def is_listen(self, event: Event):
        return self._event == event

    async def handle(self, *args, **kwargs):
        return await self._handler(*args, **kwargs)

    def __str__(self):
        return f"Listener\
                \n event: {self._event}\
                \n handler: {self._handler}"


class EventEmitterImpl(EventEmitter):
    def __init__(self):
        self._listeners = []

    def on(self, event: Event, handler: Callable):
        listener = ListenerImpl(event, handler)
        self._listeners.append(listener)

    async def emit(self, event: Event, *args, **kwargs):
        listeners = self._get_listeners(event)

        for listener in listeners:
            await listener.handle(*args, **kwargs)

    def _get_listeners(self, event: Event) -> list[Listener]:
        listeners = []

        for listener in self._listeners:
            if listener.is_listen(event):
                listeners.append(listener)

        return listeners

    def __str__(self):
        return f"\nEventEmitter\
                \nlisteners: {self._listeners} \n"
