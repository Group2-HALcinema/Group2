function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none"; // すべてのタブコンテンツを非表示にする
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", ""); // すべてのタブのactiveクラスを削除
    }

    document.getElementById(tabName).style.display = "block"; // クリックされたタブに対応するコンテンツのみを表示
    evt.currentTarget.className += " active"; // クリックされたタブにactiveクラスを追加
}

// ページ読み込み時に最初のタブを表示する
document.addEventListener('DOMContentLoaded', function() {
  openTab(null, '{{ list(showings_by_date.keys())[0] }}'); 
});