from flask import Flask, redirect, url_for
from threading import get_ident as _get_ident
from flask_admin import Admin

from app.infrastructure.db.models import Quiz, User, Question
from app.infrastructure.db.factory import create_sync_session

from ..admin.extensions import init_login
from ..admin.views.base import CustomBaseView
from ..admin.views.admin import MyAdminIndexView
from ..admin.utils import create_superuser_if_not_exists
from app.settings import get_settings, Settings


def create_app(settings: Settings) -> Flask:

    # Initialize Flask app
    app = Flask(__name__, template_folder="../admin/templates")
    app.secret_key = settings.secret_key

    # Initialize SQLAlchemy
    if settings.postgres_url is None:
        raise ValueError("Postgres URI is not set")

    Session = create_sync_session(
        url=settings.postgres_url.replace("+asyncpg", ""), scopefunc=_get_ident
    )

    app.teardown_appcontext(lambda *args: Session.remove())

    # Initialize flask-admin and login views
    admin = Admin(
        app=app,
        name="Admin",
        index_view=MyAdminIndexView(Session),
        base_template="my_master.html",
        template_mode="bootstrap4",
    )

    # Setup Views
    admin.add_view(CustomBaseView(Quiz, Session, name="Квиз"))
    admin.add_view(CustomBaseView(User, Session, name="Пользователи"))
    admin.add_view(CustomBaseView(Question, Session, name="Вопросы"))

    # Create superuser
    create_superuser_if_not_exists(Session, settings)

    # Initialize flask-login
    init_login(Session, app)

    return app


settings = get_settings()
app = create_app(settings)


@app.route("/")
def index():
    return redirect(url_for("admin.index"))
