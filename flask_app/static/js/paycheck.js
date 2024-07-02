$(document).ready(function() {
  var trigger = $('.modal__trigger'),
      wrapper = $('.modal__wrapper'),
      layer = $('.modal__layer'),
      container = $('.modal__container'),
      close = $('.modal-close');

  $(trigger).click(function() {
    var index = trigger.index(this);

    // バリデーション
    if (validateInput()) {
      // 入力内容を確認モーダルに反映
      $('#confirmName').val($('input[placeholder="お名前"]').val());
      $('#confirmEmail').val($('input[placeholder="E-Mail"]').val());
      $('#confirmPostalCode').val($('input[placeholder="郵便番号"]').val());
      $('#confirmAddress').val($('input[placeholder="住所"]').val());

      // モーダル表示
      $(wrapper).eq(index).fadeIn(400);
      $(wrapper).eq(index).find(container).scrollTop(0);
      $('html, body').css('overflow', 'hidden');
    }
  });

  $(layer).add(close).click(function() {
    $(this).closest(wrapper).fadeOut(400);
    $('html, body').removeAttr('style');
  });

  // バリデーション関数
  function validateInput() {
    var name = $('input[placeholder="お名前"]').val().trim();
    var email = $('input[placeholder="E-Mail"]').val().trim();
    var pos = $('input[placeholder="郵便番号"]').val().trim();
    var add = $('input[placeholder="住所"]').val().trim();
    var isValid = true;

    // お名前のバリデーション
    if (name === '') {
      showErrorMessage($('input[placeholder="お名前"]').closest('.cp_iptxt').find('.error-message'), '※お名前を入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="お名前"]').closest('.cp_iptxt').find('.error-message'));
    }

    // E-Mailのバリデーション 入力形式が邪魔な時は49-54行目をコメントアウト
    if (email === '') {
       showErrorMessage($('input[placeholder="E-Mail"]').closest('.cp_iptxt').find('.error-message'), '※E-Mailを入力してください。');
       isValid = false;
     } else if (!isValidEmail(email)) {
       showErrorMessage($('input[placeholder="E-Mail"]').closest('.cp_iptxt').find('.error-message'), '※正しいE-Mail形式で入力してください。');
       isValid = false;
     } else {
      hideErrorMessage($('input[placeholder="E-Mail"]').closest('.cp_iptxt').find('.error-message'));
    }

    // 郵便番号のバリデーション
    if (pos === '') {
      showErrorMessage($('input[placeholder="郵便番号"]').closest('.cp_iptxt').find('.error-message'), '※郵便番号を入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="郵便番号"]').closest('.cp_iptxt').find('.error-message'));
    }
    
    // 住所のバリデーション
    if (add === '') {
      showErrorMessage($('input[placeholder="住所"]').closest('.cp_iptxt').find('.error-message'), '※住所を入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="住所"]').closest('.cp_iptxt').find('.error-message'));
    }

    return isValid;
  }

  // エラーメッセージを表示する関数
  function showErrorMessage(element, message) {
    element.text(message).show();
  }

  // エラーメッセージを非表示にする関数
  function hideErrorMessage(element) {
    element.text('').hide();
  }

  // E-Mailの形式をチェックする関数
  function isValidEmail(email) {
    // 簡易的なメールアドレスのバリデーション
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
});