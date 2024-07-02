$(document).ready(function() {
    var selectedSeats = []; // 選択された座席のIDを格納する配列

    // 座席選択処理
    $('.seat:not(.reserved)').on('click', function() {
        var seatId = $(this).data('seat-id');
        var seatNumber = $(this).text(); 
    
        // 選択状態をトグル
        if ($(this).hasClass('selected')) { 
            $(this).removeClass('selected');
            selectedSeats = selectedSeats.filter(id => id !== seatId); // 選択解除
        } else {
            $(this).addClass('selected');
            selectedSeats.push(seatId); // 選択状態に追加
        }
    
        // 選択された座席の表示を更新
        updateSelectedSeatDisplay();
    });

    // 選択された座席の表示を更新する関数
    function updateSelectedSeatDisplay() {
        var selectedSeatText = '選択された座席: ';
        if (selectedSeats.length > 0) {
            // 選択された座席番号の配列を作成
            var selectedSeatNumbers = selectedSeats.map(function(seatId) {
                return $('.seat[data-seat-id="' + seatId + '"]').text().trim();
            });
            selectedSeatText += selectedSeatNumbers.join(', ');
        } else {
            selectedSeatText += 'なし';
        }
        $('#selected-seat').text(selectedSeatText);
    }

    // 予約ボタンクリック処理
    $('#reserve-button').click(function() {
        if (selectedSeats.length === 0) {
            $('#error-message').text('座席を選択してください');
            return;
        } else {
            $('#error-message').text('');
        }

        $.ajax({
            url: '/views/reserve_seat',
            type: 'POST',
            data: { 
                seat_ids: JSON.stringify(selectedSeats), // 配列として送信
                showing_id: 1 // 上映IDは適宜設定してください 
            },
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message);
                    $('.seat.selected').addClass('reserved').removeClass('selected');
                    selectedSeatId = null;
                } else {
                    alert(response.message);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(jqXHR, textStatus, errorThrown);

                var errorMessage = '予約に失敗しました。しばらく時間をおいてから再度お試しください。';
                if (jqXHR.responseJSON && jqXHR.responseJSON.message) {
                    errorMessage = jqXHR.responseJSON.message;
                } else if (jqXHR.status === 400) {
                    errorMessage = 'リクエストが無効です。入力内容を確認してください。';
                } else if (jqXHR.status === 500) {
                    errorMessage = 'サーバーエラーが発生しました。';
                }
                $('#error-message').text(errorMessage);
            }
        });
    });
});