from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for
from flask_login import login_user, current_user, login_required
from ..models import db, Seat, Reservation, Account, Showing, Screen
from sqlalchemy.exc import IntegrityError

views_bp = Blueprint('views', __name__, url_prefix='/views')

from flask_app import login_manager, app
print("a")

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


# 座席指定ページ
@views_bp.route('/SeatSelect')
def SeatSelect():
    # URLパラメータからshowingIDを取得
    showing_id = request.args.get('showing_id')

    if not showing_id:
        return jsonify({'status': 'error', 'message': 'URLパラメータに上映IDがありません.'}), 400
    
    # Showingテーブルからscreen_idを取得
    showing = Showing.query.get(showing_id)
    screen_id = showing.screen.ScreenID if showing else None

    if not screen_id:
        return jsonify({'status': 'error', 'message': '指定された上映IDに対応するスクリーンIDが見つかりません.'}), 400

    # データベースからスクリーンIDに一致する座席データを取得
    seats = Seat.query.filter_by(ScreenID=screen_id).all()

    # ShowingIDで予約済み座席を絞り込む
    reserved_seats = Reservation.query.filter(Reservation.ShowingID == showing_id).all()
    reserved_seat_numbers = [str(seat.SeatNumber) for seat in reserved_seats]

    # 座席データをHTMLに渡すためのリストを作成
    seat_data = []
    for seat in seats:
        seat_data.append({
            'id': seat.SeatID,
            'row': seat.Row,
            'number': seat.Number,
            'ScreenID': seat.ScreenID,
            'reserved': str(seat.Row) + str(seat.Number) in reserved_seat_numbers  # 予約済みかどうかを追加
        })

    # リクエストが AJAX リクエストかどうか判定
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX リクエストの場合、JSON 形式でレスポンス
        return jsonify({'status': 'success', 'seats': seat_data})
    else:
        # それ以外の場合は、従来通り HTML をレンダリング
        return render_template('SeatSelect.html', seats=seat_data, showing_id=showing_id)




# 座席予約機能
@views_bp.route('/reserve_seat', methods=['POST'])
@login_required
def reserve_seat():
    try:
        # フロントエンドから選択された座席IDのリストと上映IDを取得
        selected_seat_ids = request.form.getlist('seat_ids[]')  # リストとして取得
        showing_id = request.form.get('showing_id')

        # 選択された各座席に対して予約処理を実行
        for selected_seat_id in selected_seat_ids:
            # 座席IDを整数に変換してデータベースから座席情報を取得
            seat = Seat.query.get(int(selected_seat_id))  

            # 選択された座席が既に予約済みかどうかを確認
            existing_reservation = Reservation.query.filter_by(
                ShowingID=showing_id,
                SeatNumber=str(seat.Row) + str(seat.Number)
            ).first()

            # 既に予約済みの場合はエラーメッセージを返す
            if existing_reservation:
                print(existing_reservation)
                return jsonify({'status': 'error', 'message': '選択された座席は既に予約されています'}), 400

            # ログイン中のユーザーのアカウントIDを取得
            account_id = current_user.AccountID

            # 新しい予約を作成
            reservation = Reservation(
                AccountID=account_id,
                ShowingID=showing_id, 
                SeatNumber=str(seat.Row) + str(seat.Number)
            )
            db.session.add(reservation)
        
        db.session.commit()
        # リダイレクト先URLをヘッダーに含めて返す
        return jsonify({'status': 'success', 'redirect_url': url_for('views.reservation_complete')}), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")  # エラーログを出力
        return jsonify({'status': 'error', 'message': '予約に失敗しました'}), 500



@views_bp.route('/comingList')
def cominglist():
    return render_template('comingList.html')

@views_bp.route('/infoedit')
def infoedit():
    return render_template('infoEdit.html')

# 映画詳細ページ
@views_bp.route('/moviedetail')
def moviedetail():
    return render_template('moviedetail.html')

# 上映中一覧ページ
@views_bp.route('/movielist')
def movielist():
    # 上映中の映画と上映情報を取得
    # showings = db.session.query(Showing, Movie).join(Movie).all()
    # return render_template('movieList.html', showings=showings)
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

# 予約完了画面
@views_bp.route('/reservation_complete')
def reservation_complete():
    return render_template('reservation_complete.html')