from flask import Flask, render_template,Blueprint
from ..models import db, Seat

views_bp = Blueprint('views', __name__, url_prefix='/views')

# 座席指定機能作成途中　佐藤
# views_bp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # データベースのURLを設定
# db.init_app(views_bp)

@views_bp.route('/comingList')
def cominglist():
    return render_template('comingList.html')

@views_bp.route('/infoedit')
def intoedit():
    return render_template('infoEdit.html')

@views_bp.route('/moviedetail')
def moviedetail():
    return render_template('moviedetail.html')

@views_bp.route('/movielist')
def movielist():
    return render_template('movieList.html')

@views_bp.route('/screen')
def screen():
    return render_template('screen.html')

@views_bp.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

@views_bp.route('/ticketdetail')
def ticketdetail():
    return render_template('ticketDetails.html')

# 座席指定ページ
@views_bp.route('/SeatSelect')
def SeatSelect():
    return render_template('SeatSelect.html')

# 購入確認ページ
@views_bp.route('/buyCheck')
def buyCheck():
    return render_template('buyCheck.html')

# 購入完了ページ
@views_bp.route('/buycomp')
def buycomp():
    return render_template('buycomp.html')