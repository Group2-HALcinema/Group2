$(".slider").slick({
    autoplay: true, // 自動再生
    arrows: true, // 矢印
    dots: true, // インジケーター
    prevArrow: '<img src="../../static/images/slick_prevI.png" class="prev-arrow">',
    nextArrow: '<img src="../../static/images/slick_nextI.png" class="next-arrow">',
    slidesToShow: 1,
    centerMode: true,
    centerPadding: '200px',
    focusOnSelect: true,
  });