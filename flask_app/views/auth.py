from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask import render_template, url_for, redirect, flash, session, request
from flask_app import app, login_manager
from flask_app.models import *
from flask_app.views.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload
from .views import views_bp # ブループリントをインポート

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
        account =Account(Name=form.name.data, KanaName=form.kananame.data, MailAddress=form.mailaddress.data, Password=form.password.data, PhoneNumber=form.phonenumber.data, Birthday=form.birthday.data)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('signin'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f'Error in {fieldName}: {err}', 'danger')
    return render_template('signup.html', form=form)


#ログインページ
@app.route("/signin", methods=['GET', 'POST'])
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
@login_required
def signout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/memberinfo')
def memberinfo():
    return render_template('Memberinfo.html', user=current_user)

#いろいろつくる
@app.route('/seibetutukuru', methods=['GET', 'POST'])
def seibetutukuru():
    seibetu = request.form.get('seibetutukuru')
    capa = request.form.get('capacity')
    agelimit = request.form.get('agelimit')
    # a = request.form.get('a')
    # b = request.form.get('b')
    # c = request.form.get('c')
    # zaseki = [0,'A','B','C','D','E','F','G','H','I','J']
    
    if seibetu:
        seibetu = Sex(Sex=seibetu)
        db.session.add(seibetu)
        db.session.commit()
    if capa:
        capa = Screen(Capacity=capa)
        db.session.add(capa)
        db.session.commit()
    if agelimit:
        agelimit = AgeLimit(AgeLimit=agelimit)
        db.session.add(agelimit)
        db.session.commit()

    # if a:
    #     for row in range(1, 11):
    #         for col in range(1, 21):
    #             seat = Seat(Row=zaseki[row], Number=col, ScreenID=3)
    #             db.session.add(seat)
    #     db.session.commit()
    # if b:
    #     for row in range(1, 11):
    #         for col in range(1, 13):
    #             seat = Seat(Row=zaseki[row], Number=col, ScreenID=2)
    #             db.session.add(seat)
    #     db.session.commit()
    # if c:
    #     for row in range(1, 8):
    #         for col in range(1, 11):
    #             seat = Seat(Row=zaseki[row], Number=col, ScreenID=1)
    #             db.session.add(seat)
    #     db.session.commit()

    # 上映テーブルにデータを入れるやつ　佐藤
    # if request.method == 'POST':
    #     movie_id = request.form['movie_id']
    #     screen_id = request.form['screen_id']
    #     if movie_id and screen_id:
    #         new_showing = Showing(MovieID=movie_id, ScreenID=screen_id)
    #         db.session.add(new_showing)
    #         db.session.commit()


    # 予約テーブルのレコード全消し 佐藤
    # この機能を使うときは、上映テーブルにデータ入れるやつをコメントアウトしないと動かん　治す気力はない　ほかの機能止まったらごめん
    form = DeleteAllForm()
    if form.validate_on_submit():
        db.session.query(Reservation).delete()
        db.session.commit()
        return redirect(url_for('seibetutukuru'))

    reservations = Reservation.query.all()
    
    return render_template('seibetutukuru.html', reservations=reservations, form=form)

app.register_blueprint(views_bp) # ブループリントをアプリケーションに登録