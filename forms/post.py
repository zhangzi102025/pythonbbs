from .baseform import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length


class PublicPostForm(BaseForm):
    title = StringField(validators=[Length(min=2, max=100, message='标题长度为2-100')])
    content = StringField(validators=[Length(min=2, message='内容过短')])
    board_id = IntegerField(validators=[InputRequired(message='请选择版块')])


class PublicCommentForm(BaseForm):
    content = StringField(validators=[Length(min=2, max=200, message='评论长度2-200')])
