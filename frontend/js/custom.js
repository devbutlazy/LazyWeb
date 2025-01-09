$(window).on("load", function () {
    "use strict";
    $("#preloader").delay(350).fadeOut("slow");
    $(".header-inner").mCustomScrollbar();
    $(".portfolio-filter").each(function (i, buttonGroup) {
        const $buttonGroup = $(buttonGroup);
        $buttonGroup.on("click", "li", function () {
            $buttonGroup.find(".current").removeClass("current");
            $(this).addClass("current");
        });
    });
    var $container = $(".portfolio-wrapper");
    $container.imagesLoaded(function () {
        $(".portfolio-wrapper").isotope({ itemSelector: '[class*="col-"]', percentPosition: true, masonry: { columnWidth: '[class*="col-"]' } });
    });
    var curPage = 1;
    var pagesNum = $(".portfolio-pagination").find("li a:last").text();
});
$(document).on("ready", function () {
    "use strict";
    $(".testimonials-wrapper").slick({ dots: true, arrows: false, slidesToShow: 2, slidesToScroll: 2, responsive: [{ breakpoint: 768, settings: { slidesToShow: 1, slidesToScroll: 1, dots: true, arrows: false } }] });
    $(".clients-wrapper").slick({ dots: false, arrows: false, slidesToShow: 4, slidesToScroll: 4, responsive: [{ breakpoint: 768, settings: { slidesToShow: 3, slidesToScroll: 3, dots: false, arrows: false } }, { breakpoint: 425, settings: { slidesToShow: 1, slidesToScroll: 1, dots: false, arrows: false } }] });
});
$(function () {
    "use strict";
    $(".menu-icon").on("click", function () {
        $("header.left").toggleClass("open");
        $(".mobile-header, main.content").toggleClass("push");
    });
    $("main.content, header.left button.close").on("click", function () {
        $("header.left").removeClass("open");
        $(".mobile-header, main.content").removeClass("push");
    });
    $(".count").counterUp({ delay: 10, time: 2e3 });
    if ($(".skill-item").length > 0) {
        var waypoint = new Waypoint({
            element: document.getElementsByClassName("skill-item"), handler: function (direction) {
                $(".progress-bar").each(function () {
                    var bar_value = $(this).attr("aria-valuenow") + "%";
                    $(this).animate({ width: bar_value }, { easing: "linear" });
                });
                this.destroy();
            }, offset: "50%"
        });
    }
    $('.vertical-menu li a[href^="#"]:not([href="#"])').on("click", function (event) {
        var $anchor = $(this);
        $("html, body").stop().animate({ scrollTop: $($anchor.attr("href")).offset().top - 50 }, 800, "easeInOutQuad");
        event.preventDefault();
    });
    $(".vertical-menu li a").addClass("nav-link");
    $("body").scrollspy({ target: ".scrollspy", offset: 50 });
    var bg_img = document.getElementsByClassName("background");
    for (var i = 0; i < bg_img.length; i++) {
        var src = bg_img[i].getAttribute("data-image-src");
        bg_img[i].style.backgroundImage = "url('" + src + "')";
    }
    var list = document.getElementsByClassName("spacer");
    for (var i = 0; i < list.length; i++) {
        var size = list[i].getAttribute("data-height");
        list[i].style.height = "" + size + "px";
    }
    $(window).scroll(function () {
        if ($(this).scrollTop() >= 250) {
            $("#return-to-top").fadeIn(200);
        } else {
            $("#return-to-top").fadeOut(200);
        }
    });
    $("#return-to-top").on("click", function () {
        $("body,html").animate({ scrollTop: 0 }, 400);
    });
});
