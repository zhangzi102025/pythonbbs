from .baseform import BaseForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired


class AddStaffForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式不正确')])
    role = IntegerField(validators=[InputRequired(message='请选择角色')])


class EditStaffForm(BaseForm):
    is_staff = BooleanField(validators=[InputRequired(message='请选择是否为员工')])
    role = IntegerField(validators=[InputRequired(message='请选择分组')])
