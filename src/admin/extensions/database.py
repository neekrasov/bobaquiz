from flask import Flask, g
from src.db.session import sync_session


class DatabaseMiddleware:
    def __init__(self, dsn: str) -> None:
        self.sessionmaker = sync_session(dsn)

    def open(self):
        session = self.sessionmaker()
        g.session = session

    def close(self, *_args, **_kwargs):
        g.session.close()

    def register(self, app: Flask):
        app.before_request(self.open)
        app.teardown_appcontext(self.close)
