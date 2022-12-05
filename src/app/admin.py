from flask import Flask, g, redirect, url_for

from flask_admin import Admin

from src.admin.extensions import DatabaseMiddleware, init_login
from src.admin.views.base import CustomBaseView
from src.admin.views.admin import MyAdminIndexView
from src.admin.utils import create_superuser_if_not_exists
from src.core.settings import get_settings, Settings
from src.db.models import Quiz, User, QuizResult, Question


def create_app(settings: Settings) -> Flask:
    # Initialize Flask app
    app = Flask(__name__, template_folder="../admin/templates")
    app.secret_key = settings.secret_key

    # Register middleware
    if settings.postgres_uri is None:
        raise ValueError("Postgres URI is not set")

    dbm = DatabaseMiddleware(settings.postgres_uri.replace("+asyncpg", ""))
    dbm.register(app)

    # Initialize flask-admin
    admin = Admin(
        app=app,
        name="Admin",
        index_view=MyAdminIndexView(),
        base_template="my_master.html",
        template_mode="bootstrap4",
    )

    with app.app_context():
        if "session" not in g:
            dbm.open()
        session = g.session

        # Setup Views
        admin.add_view(CustomBaseView(Quiz, session, name="Квиз"))
        admin.add_view(CustomBaseView(User, session, name="Пользователи"))
        admin.add_view(CustomBaseView(QuizResult, session, name="Результаты"))
        admin.add_view(CustomBaseView(Question, session, name="Вопросы"))

        # Create superuser
        create_superuser_if_not_exists(session, settings)

        # Initialize flask-login
        init_login(session, app)

    return app


settings = get_settings()
app = create_app(settings)


@app.route("/")
def index():
    return redirect(url_for("admin.index"))
