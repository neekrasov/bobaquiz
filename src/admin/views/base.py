import flask_login as login
from flask_admin.contrib.sqla import ModelView


class CustomBaseView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    column_sortable_list = ['created_at', 'updated_at']
    
    def is_accessible(self):
        return login.current_user.is_authenticated