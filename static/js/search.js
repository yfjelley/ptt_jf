function search() {
    var keyword = $('#search').val();
    var dst = "/bbs/search/" + keyword + "/";
    if (keyword != '') {
        window.location = dst;
    } else {
        return false;
    };
}

$(document).ready(function(){
    $('#search-btn').click(
        function(){
          search();
        }
    );
});
