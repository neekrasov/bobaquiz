from flask import g
from wtforms import form, fields, validators
from src.db.models import User
from fastapi_users.password import PasswordHelper


class LoginForm(form.Form):
    login = fields.StringField()
    password = fields.PasswordField()
    passw_helper = PasswordHelper()

    def validate_login(self, field):
        user = self.get_user()
        print(user)

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not self.passw_helper.verify_and_update(self.password.data, user.hashed_password):
            raise validators.ValidationError('Invalid password')
        
        if user.is_active is False:
            raise validators.ValidationError('User is not active')
        
        if not user.is_staff or not user.is_superuser:
            raise validators.ValidationError('You do not have permission to access the admin panel')

    def get_user(self):
        return g.session.query(User).filter_by(username=self.login.data).first()