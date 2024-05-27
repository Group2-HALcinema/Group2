from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import flash
from wtforms import *
from wtforms.validators import DataRequired, Length, EqualTo
from flask_app.models import *

class SignUpForm(FlaskForm):
    name = StringField('氏名', validators=[DataRequired(), Length(min=2, max=20)])
    pronname = StringField('カナ', validatord=[DataRequired()])
    password  = PasswordField('パスワード', validators=[DataRequired()])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password')])
    mailaddress = StringField('メールアドレス', validators=[DataRequired()])
    phonenumber = StringField('電話番号', validators=[DataRequired(), Length(min=6, max=13)])
    birthday = DateField('生年月日', format='%Y/%m/%d')
    submit = SubmitField('サインアップ')
    def validate_password(self, field):
        if field.data == self.name.data:
            raise flash("氏名と同じパスワードは使用できません")
    
class LoginForm(FlaskForm):
    username = StringField('メールアドレス', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')