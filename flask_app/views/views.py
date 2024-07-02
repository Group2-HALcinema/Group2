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
    # # データベースから座席データを取得
    # seats = Seat.query.all()

    # # 座席データをHTMLに渡すためのリストを作成
    # seat_data = []
    # for seat in seats:
    #     seat_data.append({
    #         'id': seat.id,
    #         'row': seat.Row,
    #         'number': seat.Number,
    #         'reserved': seat.is_reserved,
    #     })

    
    # 10行20列の座席データ (A1-A20, B1-B20, ..., J1-J20)
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    columns = 20

    # 座席データをHTMLに渡すためのリストを作成
    seat_data = []
    id = 1
    for row in rows:
        for number in range(1, columns + 1):
            # データベースから予約状況を取得
            seat = Seat.query.filter_by(Row=row, Number=number).first()
            reserved = seat.is_reserved if seat else False  # seat が None の場合は予約なし

            seat_data.append({
                'id': id,
                'row': row,
                'number': number,
                'reserved': reserved,
            })
            id += 1

    return render_template('SeatSelect.html', seats=seat_data)

@views_bp.route('/reserve_seat', methods=['POST'])
@login_required
def reserve_seat():
    try:
        selected_seat_id = request.form.get('seat_id')  # formから取得
        showing_id = request.form.get('showing_id')  # formから取得

        seat = Seat.query.get(selected_seat_id)
        if not seat:
            print(f"Seat not found for ID: {selected_seat_id}") # seat が None の場合に出力
        elif seat.is_reserved:
            print(f"Seat already reserved: {seat.id}") # seat が予約済みの場合に出力

        seat = Seat.query.get(selected_seat_id)
        if not seat or seat.is_reserved:
            return jsonify({'status': 'error', 'message': 'この座席は予約できません'}), 400

        account_id = current_user.AccountID

        reservation = Reservation(
            AccountID=account_id,
            ShowingID=showing_id, 
            SeatNumber=str(seat.Row) + str(seat.Number),
            # PriceID=...,  # 必要に応じて設定
            # DiscountID=...  # 必要に応じて設定
        )
        db.session.add(reservation)

        # 座席を予約済みにする
        seat.is_reserved = True
        db.session.commit()

        return jsonify({'status': 'success', 'message': '座席を予約しました'})
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")  # エラーログを出力
        # return jsonify({'status': 'error', 'message': '予約に失敗しました'}), 500
        return jsonify({'status': 'error', 'message': str(e)}), 500  # エラーメッセージを返す


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

# お支払確認ページ　ついかこんどう
@views_bp.route('/paycheck')
def paycheck():
    return render_template('paycheck.html')