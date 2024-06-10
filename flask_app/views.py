from flask import render_template, url_for, redirect, flash, session, request
from flask_app import app, login_manager
from flask_app.models import *
from flask_app.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

#インデックス
@app.route("/")
def index():
    return render_template("top.html")

#アカウント作成
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        account =Account(Name=form.name.data, Kananame=form.kananame.data, MailAddress=form.mailaddress.data, Password=form.password.data, Phonenumber=form.phonenumber.data, Birthday=form.birthday.data)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


#ログインページ
@app.route("/signin")
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(Name=form.name.data).first()
        if account and account.Password == form.password.data:
            login_user(account)
            return redirect(url_for('index'))
        else:
            flash('ログインに失敗しました', 'danger')
    return render_template('signin.html', form=form)

#ログアウト
@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index'))