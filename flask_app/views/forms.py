from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from wtforms import *
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_app.models import *
from flask_app.views import auth

forms_bp = Blueprint('forms', __name__, url_prefix='/forms')

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

class DeleteAllForm(FlaskForm):
    submit = SubmitField('すべて削除')
    
# ログインしているユーザーのデータを更新する
@forms_bp.route("/prof_update", methods=["GET", "POST"])
def prof_update():
    if 'user_id' not in session:
        flash('ログインしてください', 'warning')
        return redirect(url_for('signin'))
    
    user = Account.query.get(session['user_id'])

    if request.method == 'POST':
        # フォームからデータを取得
        name = request.form.get("Name")
        kananame = request.form.get("KanaName")
        password = request.form.get("Password")
        mailaddress = request.form.get("MailAddress")
        phonenumber = request.form.get("PhoneNumber")

        # 取得したデータを現在のユーザーデータに更新
        if name:
            user.name = name
        if kananame:
            user.kananame = kananame
        if password:
            user.set_password(password)  # パスワードのハッシュ化を考慮
        if mailaddress:
            user.mailaddress = mailaddress
        if phonenumber:
            user.phonenumber = phonenumber

        # データベースに変更をコミット
        try:
            db.session.commit()
            flash('プロフィールが更新されました', 'success')
        except:
            db.session.rollback()
            flash('プロフィールの更新に失敗しました', 'danger')
        
        return redirect(url_for('memberinfo'))

    return render_template('MemberInfo.html', user=user)