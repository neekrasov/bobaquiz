import flask_login as login

from app.infrastructure.db.models import User


# Initialize flask-login
def init_login(session, app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        return user
