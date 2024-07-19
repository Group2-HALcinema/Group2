from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from wtforms import *
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_app.models import *
from flask_app.views import auth

from flask_login import current_user
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

class AddressForm(FlaskForm):
    """住所入力フォーム"""
    PostNumber = StringField('郵便番号', validators=[DataRequired(message='郵便番号は必須です'), Length(min=7, max=7, message='7桁の数字を入力してください')])
    Todohuken = StringField('都道府県', validators=[DataRequired(message='都道府県は必須です')])
    Shiku = StringField('市区町村', validators=[DataRequired(message='市区町村は必須です')])
    ChosonNumber = StringField('番地', validators=[DataRequired(message='番地は必須です')])
    submit = SubmitField('登録')

class AccountForm(FlaskForm):
    name = StringField('氏名', validators=[DataRequired()], default=lambda: current_user.Name if current_user.is_authenticated else '')
    kananame = StringField('フリガナ', validators=[DataRequired()], default=lambda: current_user.KanaName if current_user.is_authenticated else '')
    mailaddress = StringField('メールアドレス', validators=[DataRequired(), Email()], default=lambda: current_user.MailAddress if current_user.is_authenticated else '')
    password = PasswordField('パスワード') # 入力があれば更新
    phonenumber = TelField('電話番号', default=lambda: current_user.PhoneNumber if current_user.is_authenticated else '')
    submit = SubmitField('更新')


# authに移動する
# ログインしているユーザーのデータを更新する
@forms_bp.route("/prof_update", methods=["GET", "POST"])
def prof_update():
    """ユーザーの個人情報を更新する."""

    # ログイン済みユーザーかどうかを確認
    if not current_user.is_authenticated:
        flash('このページにアクセスするにはログインしてください。', 'danger')
        return redirect(url_for('signup'))

    form = AccountForm(obj=current_user)  # フォームに現在のユーザー情報を反映
    if current_user.is_authenticated:
        # ログインしているユーザーのデータを取得
        user_data = Account.query.filter_by(id=current_user.id).first()
                # フォームにユーザーデータを設定
        form.name.data = user_data.Name
        form.kananame.data = user_data.KanaName
        form.mailaddress.data = user_data.MailAddress
        form.phonenumber.data = user_data.PhoneNumber

    if form.validate_on_submit():
        try:
            # ユーザー情報を更新
            current_user.name = form.name.data
            current_user.kananame = form.kananame.data
            current_user.mailaddress = form.mailaddress.data
            # パスワードが設定されていれば更新
            if form.password.data:
                current_user.password = form.password.data
            current_user.phonenumber = form.phonenumber.data

            db.session.commit()
            flash('プロフィールが更新されました。', 'success')
            return redirect(url_for('index'))  # ホーム画面など適切なページへリダイレクト
        except Exception as e:
            db.session.rollback()
            flash('プロフィールの更新に失敗しました。', 'danger')
            print(e)  # エラー内容をログ出力

    return render_template('MemberInfo.html', form=form, user=current_user)

# authに移動する
@app.route('/memberinfo', methods=["GET", "POST"])
def memberinfo():
    reservations = Reservation.query.filter_by(AccountID=current_user.get_id()).all()
    # form を render_template に渡す
    form = AccountForm(obj=current_user)
    return render_template('Memberinfo.html', user=current_user, reservations=reservations, form=form)