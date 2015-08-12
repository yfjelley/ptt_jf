$(function() {
var top = $('#rightSidebar').offset().top - parseFloat($('#rightSidebar').css('marginTop').replace(/auto/, 0));
var footTop = $('#footer').offset().top - parseFloat($('#footer').css('marginTop').replace(/auto/, 0));
 
var maxY = footTop - $('#rightSidebar').outerHeight();

$(window).scroll(function(evt) {
var y = $(this).scrollTop();
if (y > top) {
if (y < maxY) {
$('#rightSidebar').addClass('fixed').removeAttr('style');
} else {
$('#rightSidebar').removeClass('fixed').css({
position: 'absolute',
top: (maxY - top) + 'px'
});
}
} else {
$('#rightSidebar').removeClass('fixed');
}
});
});