import flask_login as login
from flask import url_for, redirect, request
from flask_admin import helpers, expose, AdminIndexView
from sqlalchemy.orm import scoped_session

from ..forms.login import LoginForm


class MyAdminIndexView(AdminIndexView):
    def __init__(self, session: scoped_session, *args, **kwargs):
        self.session = session
        super(MyAdminIndexView, self).__init__(*args, **kwargs)

    @expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        form = LoginForm(data=request.form, session=self.session)

        if helpers.validate_form_on_submit(form):
            login.login_user(form.get_user(session=self.session))

        if login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        self._template_args["form"] = form
        return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))
