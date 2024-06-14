from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import flash
from wtforms import *
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_app.models import *

class SignUpForm(FlaskForm):
    name = StringField('氏名', validators=[DataRequired(), Length(min=2, max=20)])
    kananame = StringField('カナ', validators=[DataRequired()])
    mailaddress = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password')])
    sex = SelectField('性別', coerce=int)
    phonenumber = StringField('電話番号', validators=[DataRequired(), Length(min=6, max=13)])
    birthday = DateField('生年月日', format='%Y/%m/%d')
    submit = SubmitField('サインアップ')

    def validate_password(self, field):
        if field.data == self.name.data:
            raise ValidationError("氏名と同じパスワードは使用できません")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.sex.choices = [(c.SexID, c.Sex) for c in Sex.query.all()]

    
class SigninForm(FlaskForm):
    name = StringField('メールアドレス', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')