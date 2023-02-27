from flask_wtf.file import FileAllowed
from wtforms import StringField, ValidationError, BooleanField, FileField
from wtforms.validators import Email, EqualTo, Length
from exts import cache
from .baseform import BaseForm
from models.user import UserModel


# 继承基础表单类BaseForm
class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误')])
    captcha = StringField(validators=[Length(min=4, max=4, message='验证码格式错误')])
    username = StringField(validators=[Length(min=2, max=20, message='用户名长度2-20')])
    password = StringField(validators=[Length(min=6, max=20, message='密码名长度6-20')])
    confirm_password = StringField(validators=[EqualTo('password', message='两次密码不一致')])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message='邮箱已经存在')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or captcha != cache_captcha:
            raise ValidationError(message='验证码错误')


# 登陆表单验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误')])
    password = StringField(validators=[Length(min=6, max=20, message='密码长度错误')])
    remember = BooleanField()


class EditProfileForm(BaseForm):
    username = StringField(validators=[Length(min=2, max=20, message='用户名长度2-20')])
    avatar = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message='文件类型错误')])
    signature = StringField()

    def validate_signature(self, field):
        signature = field.data
        if signature and len(signature) > 100:
            raise ValidationError(message='签名长度最长100')
