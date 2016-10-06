/* 
    custom.js
    description: custom js style
    created by: ann keenan
*/

$(document).ready(function () {
    $(".navbar-nav li a").click(function(event) {
        $(".navbar-collapse").collapse('hide');
    });
});

$(window).on("resize", function() {
    if ($(window).width() >= 768) {
        $(".header-img").attr("src", "{% static 'img/background.png' %}");
    } else {
        $(".header-img").attr("src", "{% static 'img/background-mobile.png' %}");
    }
}).resize();