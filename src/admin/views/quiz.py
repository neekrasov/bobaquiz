from flask_admin.contrib.sqla import ModelView
from flask_admin.model.form import InlineFormAdmin

class QuizView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['id', 'name']

    column_sortable_list = ['created_at', 'updated_at']


class QuizInlineAdmin(InlineFormAdmin):
    form_excluded_columns = ['id', 'name']