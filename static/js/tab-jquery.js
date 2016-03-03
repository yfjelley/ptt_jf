;(function($){
    $.fn.tab = function(options) {
        var defaults = {
            'type' : 'cl',
            'state': 0
        };
        var member = {
            'nav' : null,
            'con' : null
        };
        var settings = $.extend({},defaults, options);
        buildMember(this,member);
        return this.each(function(){
            member.nav.each(function(index){
                var _this = $(this);
                _this.ind = index;
                if(settings.type == 'mo'){
                    $(this).mouseover(function(){
                        act($(this),member,_this.ind);
                    });
                }else{
                    $(this).click(function(){
                        act($(this),member,_this.ind);
                    });
                }
            });
        });
    };
    /**
     * 获取tab和con对象。
     * @param  {[type]} obj [description]
     * @param  {[type]} m   [description]
     */
    function buildMember(obj,m){
        m.nav = obj.find('.tabs-nav li');
        m.con = obj.find('.tabs-cont');
    }
    function act(obj,m,index){
        obj.addClass('current').siblings().removeClass('current');
        m.con.eq(index).addClass('current').siblings().removeClass('current');
    }
})(jQuery);



