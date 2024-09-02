from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for
from flask_login import login_user, current_user, login_required
from ..models import db, Seat, Reservation, Account, Showing, Screen, Movie, Price
from sqlalchemy.exc import IntegrityError
import re
views_bp = Blueprint('views', __name__, url_prefix='/views')

from flask_app import login_manager, app

# 座席指定機能作成途中　佐藤
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/HALcinema.db'  # データベースのURLを設定

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

# 座席指定ページ(表示)
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
        print(seats)
        return render_template('SeatSelect.html', seats=seat_data, showing_id=showing_id,screen_id=screen_id)


# 座席指定ページ(座席予約機能)
@views_bp.route('/reserve_seat', methods=['POST'])
@login_required
def reserve_seat():
    try:
        # フロントエンドから選択された座席IDのリストと上映IDを取得
        selected_seat_str = request.form.get('selected_seats')  # リストとして取得
        showing_id = request.form.get('showing_id')
        price_plans = request.form.getlist('price_plans')  
        
        print("選択された料金プラン:", price_plans)
        print("受け取った座席ID:", selected_seat_str)
        print("受け取ったShowingID:", showing_id)
        
        
        # selected_seat_str の内容を確認する
        if selected_seat_str:
            print(f"selected_seat_str の型: {type(selected_seat_str)}")
            print(f"selected_seat_str の内容: {selected_seat_str}")

        # 正規表現を使って座席IDを抽出
        seat_id_matches = re.findall(r'<Seat (\d+)>', selected_seat_str)
        if not seat_id_matches:
            return jsonify({'status': 'error', 'message': '座席IDの形式が不正です'}), 400
        
        selected_seat_list = seat_id_matches
        print(f"抽出後の selected_seat_list: {selected_seat_list}")
        
        # `showing_id` から数値を抽出
        showing_id_match = re.search(r'\d+', showing_id)
        if showing_id_match:
            showing_id = int(showing_id_match.group())
        else:
            return jsonify({'status': 'error', 'message': 'ShowingIDの形式が不正です'}), 400

        # 料金プランが二重リストで渡されている場合の処理
        if isinstance(price_plans[0], str):
            import ast
            price_plans = ast.literal_eval(price_plans[0])
        
        if len(selected_seat_list) != len(price_plans):
            return jsonify({'status': 'error', 'message': '座席と料金プランの数が一致しません'}), 400
    
        # 選択された各座席に対して予約処理を実行
        for selected_seat_id, price_plan_id in zip(selected_seat_list, price_plans):
            
            
            seat = Seat.query.filter_by(SeatID=selected_seat_id).first()
            if seat is None:
                return jsonify({'status': 'error', 'message': f'Seat ID {selected_seat_id} が存在しません'}), 400

            # 選択された座席が既に予約済みかどうかを確認
            existing_reservation = Reservation.query.filter_by(
                ShowingID=showing_id,
                SeatNumber=str(seat.Row) + str(seat.Number)
            ).first()

            # 既に予約済みの場合はエラーメッセージを返す
            if existing_reservation:
                return jsonify({'status': 'error', 'message': '選択された座席は既に予約されています'}), 400

            # ログイン中のユーザーのアカウントIDを取得
            account_id = current_user.AccountID

            # 新しい予約を作成
            reservation = Reservation(
                AccountID=account_id,
                ShowingID=showing_id, 
                SeatNumber=str(seat.Row) + str(seat.Number),
                PriceID=price_plan_id
            )
            db.session.add(reservation)
        
        db.session.commit()
        # リダイレクト先URLをヘッダーに含めて返す
        return redirect('buycomp')
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")  # エラーログを出力
        return jsonify({'status': 'error', 'message': str(e)}), 500  # エラーメッセージを返す


# 公開予定一覧ページ
@views_bp.route('/comingList')
def cominglist():
    # Showingテーブルに存在するMovieIDを取得
    showing_movie_ids = db.session.query(Showing.MovieID).distinct().all()
    showing_movie_ids = [item[0] for item in showing_movie_ids]

    # Showingテーブルに存在しないMovieIDを持つ映画情報を取得
    upcoming_movies = db.session.query(Movie).filter(~Movie.MovieID.in_(showing_movie_ids)).all()
    return render_template('comingList.html',upcoming_movies=upcoming_movies)


@views_bp.route('/infoedit')
def infoedit():
    return render_template('infoEdit.html')

# 映画詳細ページ
@views_bp.route('/moviedetail/<int:movie_id>')
def moviedetail(movie_id):
    # movie_idに基づいて映画の情報を取得
    movie = Movie.query.get_or_404(movie_id)
    showing = Showing.query.all()
    return render_template('moviedetail.html', movie=movie, showing=showing)

# 上映中一覧ページ
@views_bp.route('/movielist')
def movielist():
    # Showingテーブルから上映中のMovieIDを取得
    showing_movie_ids = db.session.query(Showing.MovieID).distinct().all()
    showing_movie_ids = [item[0] for item in showing_movie_ids]  # リスト内のタプルを展開

    # 取得したMovieIDリストを使ってMovieテーブルから映画情報を取得
    movies = db.session.query(Movie).filter(Movie.MovieID.in_(showing_movie_ids)).all()

    return render_template('movieList.html', movies=movies)


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
    showing_id = request.args.get('showing_id')
    selected_seat_str = request.args.get('selected_seats')  # リストとして取得
    
    print("受け取ったShowingID:", showing_id)

    if not showing_id:
        return jsonify({'status': 'error', 'message': 'URLパラメータに上映IDがありません.'}), 400
    
    # Showingテーブルからshowing情報を取得
    showing = Showing.query.get(showing_id)

    if not showing:
        return jsonify({'status': 'error', 'message': '指定された上映IDに対応する上映情報が見つかりません.'}), 400
    
    # 選択された座席IDをリストに変換
    try:
        selected_seat_ids = [int(seat_id) for seat_id in selected_seat_str.split(',') if seat_id]
    except ValueError:
        return jsonify({'status': 'error', 'message': '座席IDの形式が無効です。'}), 400

    # 選択された座席情報を取得
    selected_seats_info = []
    for selected_seat_id in selected_seat_ids:
        seat = Seat.query.get(selected_seat_id)
        if seat:
            selected_seats_info.append(seat)
    
    price = Price.query.all()
    
    return render_template('buyCheck.html', showing=showing, selected_seats=selected_seats_info, price=price, showing_id=showing)


# 購入完了ページ
@views_bp.route('/buycomp')
def buycomp():
    return render_template('buycomp.html')

# お支払確認ページ　ついかこんどう
@views_bp.route('/paycheck', methods=['POST'])
def paycheck():
    selected_seat_str = request.form.get('selected_seats')  # リストとして取得
    showing_id = request.form.get('showing_id')
    price_plans = request.form.getlist('price_plans[]')  # フォームデータの確認
    
    # 選択された座席IDをリストに変換
    # try:
    #     selected_seat_ids = [int(seat_id) for seat_id in selected_seat_str.split(',') if seat_id]
    # except ValueError:
    #     return jsonify({'status': 'error', 'message': '座席IDの形式が無効です。'}), 400
    
    # 選択された座席情報を取得
    # selected_seats_info = []
    # for selected_seat_id in selected_seat_str:
    #     seat = Seat.query.get(selected_seat_id)
    #     if seat:
    #         selected_seats_info.append(seat)
    
    print("選択された料金プラン:", price_plans)
    print("受け取った座席ID:", selected_seat_str)
    print("受け取ったShowingID:", showing_id)
    
    return render_template('paycheck.html', price_plans=price_plans, showing_id=showing_id, selected_seats=selected_seat_str)

# 予約完了画面
@views_bp.route('/reservation_complete')
def reservation_complete():
    return render_template('reservation_complete.html')