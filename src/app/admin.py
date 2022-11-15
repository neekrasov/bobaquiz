from flask import Flask
from flask_admin import Admin, AdminIndexView

from src.core.settings import get_settings
from src.db.models import Quiz, User, QuizResult
from flask_admin.contrib.sqla import ModelView
from src.admin.views.quiz import QuizView
from src.db.session import sync_session


def create_app(current_session) -> Flask:
    app = Flask(__name__)
    app.secret_key = get_settings().secret_key
    admin = Admin(
        app=app, 
        name='Admin', 
        index_view=AdminIndexView(name='📃', url='/'), 
        template_mode='bootstrap4'
    )
    
    admin.add_view(QuizView(Quiz, current_session, name='Квиз'))
    admin.add_view(ModelView(User, current_session, name='Пользователи'))
    admin.add_view(ModelView(QuizResult, current_session, name='Результаты'))

    return app

if (uri := get_settings().postgres_uri) is not None:
    global app
    print('Starting admin app on uri:', uri)
    app = create_app(sync_session(
        uri.replace("+asyncpg", "")
    ))