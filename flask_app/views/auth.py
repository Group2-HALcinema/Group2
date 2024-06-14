# from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask import render_template, url_for, redirect, flash, session, request
from flask_app import app, login_manager
from flask_app.models import *
from flask_app.views.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload

# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

#インデックス
# @auth_bp.route("/")
# def index():
#     return render_template("top.html")
@app.route("/")
def index():
    return render_template('top.html')

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

@app.route('/comingList')
def cominglist():
    return render_template('comingList.html')

@app.route('/infoedit')
def intoedit():
    return render_template('infoEdit.html')

@app.route('/memberinfo')
def memberifo():
    return render_template('Memberinfo.html')

@app.route('/moviedetail')
def moviedetail():
    return render_template('moviedetail.html')

@app.route('/movielist')
def movielist():
    return render_template('movieList.html')

@app.route('/screen')
def screen():
    return render_template('screen.html')

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

@app.route('/ticketdetail')
def ticketdetail():
    return render_template('ticketDetails.html')

