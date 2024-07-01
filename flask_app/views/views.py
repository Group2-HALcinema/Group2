from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for
from flask_login import login_user, current_user, login_required
from ..models import db, Seat, Reservation, Account
from sqlalchemy.exc import IntegrityError

views_bp = Blueprint('views', __name__, url_prefix='/views')

from flask_app import login_manager, app

# 座席指定機能作成途中　佐藤
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/HALcinema.db'  # データベースのURLを設定

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

# 座席指定ページ
@views_bp.route('/SeatSelect')
def SeatSelect():
    seats = Seat.query.all()
    return render_template('SeatSelect.html', seats=seats)

from sqlalchemy.exc import IntegrityError

@views_bp.route('/reserve_seat', methods=['POST'])
@login_required
def reserve_seat():
    selected_seat_id = request.get_json()['seat_id']
    seat = Seat.query.get(selected_seat_id)

    if seat and not seat.is_reserved:
        account_id = current_user.AccountID
        try:
            reservation = Reservation(
                AccountID=account_id,
                ShowingID=1,
                SeatNumber=str(seat.Row) + str(seat.Number),
                PriceID=1,
                DiscountID=1
            )
            db.session.add(reservation)
            db.session.commit()
            return jsonify({'status': 'success', 'message': '座席を予約しました'})
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
            return jsonify({'status': 'error', 'message': '予約に失敗しました'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'この座席は予約できません'}), 400



@views_bp.route('/comingList')
def cominglist():
    return render_template('comingList.html')

@views_bp.route('/infoedit')
def infoedit():
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

# 購入確認ページ
@views_bp.route('/buyCheck')
def buyCheck():
    return render_template('buyCheck.html')

# 購入完了ページ
@views_bp.route('/buycomp')
def buycomp():
    return render_template('buycomp.html')