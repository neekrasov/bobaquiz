from wtforms import form, fields, validators
from src.db.models import User
from passlib.exc import UnknownHashError
from passlib.context import CryptContext
from sqlalchemy.orm import scoped_session


class LoginForm(form.Form):

    def __init__(self, session: scoped_session, *args, **kwargs):
        self.session = session
        super(LoginForm, self).__init__(*args, **kwargs)

    login = fields.StringField()
    password = fields.PasswordField()
    passw_helper = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def validate_login(self, field):
        user = self.get_user(self.session)

        if user is None:
            raise validators.ValidationError("Invalid user")

        try:
            verify_password = self.passw_helper.verify(
                self.password.data, user.hashed_password
            )
        except UnknownHashError:
            verify_password = False

        if not verify_password:
            raise validators.ValidationError("Invalid password")

        if user.is_active is False:
            raise validators.ValidationError("User is not active")

        if not user.is_staff:
            if user.is_superuser:
                return
            raise validators.ValidationError(
                "You do not have permission to access the admin panel"
            )

    def get_user(self, session):
        return (
            session.query(User).filter_by(username=self.login.data).first()
        )
