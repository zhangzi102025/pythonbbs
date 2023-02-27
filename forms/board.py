from wtforms import StringField, IntegerField
from wtforms.validators import Length, InputRequired, ValidationError

from forms.baseform import BaseForm
from models.post import BoardModel


class EditBoardForm(BaseForm):
    name = StringField(validators=[Length(min=2, max=20, message='版块长度为2-20')])