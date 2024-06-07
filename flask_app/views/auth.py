from flask import render_template, url_for, redirect, flash, session, request
from flask_app import app, login_manager
from flask_app.models import *
from flask_app.views.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

#インデックス
@app.route("/")
def index():
    return render_template("index.html")

#アカウント作成
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user =Account(name=form.name.data, pronname=form.pronname.data, mailaddress=form.mailaddress.data, password=form.password.data, phonenumber=form.phonenumber.data, birthday=form.birthday.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))
    return render_template('signup.html', form=form)


#ログインページ
@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('ログインに失敗しました', 'danger')
    return render_template('login.html', form=form)

#ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))