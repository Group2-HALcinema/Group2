<<<<<<< HEAD
$(document).ready(function() {
    // 座席データの取得（仮データ）
    // 非同期でサーバーから取得する必要がある
    var seats = [];

    // 20*10の座席データ
    const rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'];
    const columns = 10;

    let id = seats.length + 1; // 既存データのIDの続きから始める

    for (let row of rows) {
        for (let number = 1; number <= columns; number++) {
            // 既存の座席データに追加されないようにチェック
            if (!seats.some(seat => seat.row === row && seat.number === number)) {
                seats.push({ id: id++, row: row, number: number, reserved: false });
            }
        }
    }

    console.log(seats);

    // 座席マップの生成
    var seatMap = $('#seat-map');
    $.each(seats, function(index, seat) {
        var seatElement = $('<div>')
            .addClass('seat')
            .attr('data-seat-id', seat.id)
            .text(seat.row + seat.number); // 座席番号を表示

        if (seat.reserved) {
            seatElement.addClass('reserved');
        }

        seatMap.append(seatElement);
    });

    // 座席選択処理
    var selectedSeatId = null;
    seatMap.on('click', '.seat:not(.reserved)', function() {
        // 以前選択していた座席をリセット
        $('.seat.selected').removeClass('selected');

        // クリックした座席を選択状態にする
        $(this).addClass('selected');
        selectedSeatId = $(this).data('seat-id');
    });

    // 予約ボタンクリック処理
    $('#reserve-button').click(function() {
        if (selectedSeatId === null) {
            // 座席が選択されていない場合のエラーはここに表示
            $('#error-message').text('座席を選択してください'); 
            return;
        } else {
            // エラーメッセージをリセット
            $('#error-message').text('');
        }
        

        // サーバーに予約リクエストを送信
        $.ajax({
            url: '/reserve_seat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ seat_id: selectedSeatId }),
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message);
                    // 予約が成功したら、選択状態をリセットしたり、画面遷移したりする
                    // 選択された座席に'reserved'クラスを追加
                    $('.seat.selected').addClass('reserved').removeClass('selected');
                    // 選択状態をリセット
                    selectedSeatId = null;
                } else {
                    alert(response.message);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(jqXHR, textStatus, errorThrown); // コンソールにエラー情報を出力
                // サーバーからエラーメッセージを取得できる場合は表示する
                if (jqXHR.responseJSON && jqXHR.responseJSON.message) {
                    $('#error-message').text(jqXHR.responseJSON.message);
                }
            }
        });
    });
});
=======
>>>>>>> 708d1474a4d58829f9c6977a7832ba78fc9e30d9
