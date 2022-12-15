from typing import Protocol


class Listener(Protocol):
    def is_listen(self, event):
        ...

    def handle(self, *args, **kwargs):
        ...


class EventEmitter(Protocol):
    def on(self, event, handler):
        ...

    def emit(self, event, *args, **kwargs):
        ...

    def _get_listeners(self, event):
        ...
