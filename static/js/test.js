$(function () {
    //初始化选择项
    var str_lo = window.location.href;
    lo_arr = str_lo.split("?");
    if (lo_arr.length > 1) {
        var row = lo_arr[1].split("&");
        for (var i = 0; i < row.length; i++) {
            var obj = row[i].split("=");
            switch (obj[0]) {
                case "grade":
                    $(".pbox_con ul li").eq(0).children(".info_con").children("a").removeClass("btn_blue_").eq(obj[1]).addClass("btn_blue_");
                    break;
                case "overall":
                    $(".pbox_con ul li").eq(1).children(".info_con").children("a").removeClass("btn_blue_").eq(obj[1]).addClass("btn_blue_");
                    break;
                case "time":
                    $(".pbox_con ul li").eq(2).children(".info_con").children("a").removeClass("btn_blue_").eq(obj[1]).addClass("btn_blue_");
                    break;
            }
        }
    }

    function init() {
        //login关闭按钮
        $("#close").on("click", function () {
            $(".login-box").hide();
            $("._login_div_filter_").hide();

        });
        //初始化投资偏好
        $(".dropBtn").on("click", function () {
            $(this).next("ul").show();
        });

        $(".grade").live("mouseover", function () {
            $(this).next(".th-icon-ul").show();
        });
        $(".grade").live("mouseout", function () {
            $(this).next(".th-icon-ul").hide();
        });
        //悬停保障等级显示右侧
        // $(".grade").hover(function(){
        //     $(this).next(".th-icon-ul").show();
        // },function(){
        //     $(this).next(".th-icon-ul").hide();
        // });
        //点击保障等级,年化收益，投资期限显示状态
        $(".info_con a").on("click", function () {
            //给当前A标签添加class btn_blue_,当前dom元素兄弟姐级删除Class btn_blue_
            $(this).addClass("btn_blue_").siblings("a").removeClass("btn_blue_");
            nowcheckparam();
        });
        //排序点击
        $(".px_box ul li a").on("click", function () {
            //本身添加class属性 active 父级dom节点的兄弟级的子级节点删除active
            $(this).addClass("active").parent("li").siblings("li").children("a").removeClass("active");
            //存在i标签及修改i标签箭头
            if ($(this).children("i").length > 0) {
                //判断i节点的class 为i-active 改为i-active-2,反之改回
                if ($(this).children("i").attr("class") == "i-active") {
                    $(this).children("i").attr("class", "i-active-2");
                    $(this).attr("sortorder", "asc");
                } else if ($(this).children("i").attr("class") == "i-active-2") {
                    $(this).children("i").attr("class", "i-active");
                    $(this).attr("sortorder", "desc");
                } else {
                    //本身的dom子节点添加class属性i-active ，父级的a的父级的li的兄弟级的li的子节点的a的子节点的i的删除节点i-active
                    $(this).children("i").addClass("i-active").parent("a").parent("li").siblings("li").children("a").children("i").removeClass("i-active");
                }
            }
            nowcheckparam();

        });

    }

    init();

});

//获取当前用户选择给予传参
function nowcheckparam() {
    var grade = $(".pbox_con ul li").eq(0).children(".info_con").children(".btn_blue_").attr("grade");
    var overall = $(".pbox_con ul li").eq(1).children(".info_con").children(".btn_blue_").attr("overall");
    var time = $(".pbox_con ul li").eq(2).children(".info_con").children(".btn_blue_").attr("time");
    var sorttype = $(".px_box ul li").children(".active").attr("sorttype");
    var sortorder = $(".px_box ul li").children(".active").attr("sortorder");
    var operation = 'sort';
    var url = 'http://www.touzhijia.com/platform/lists';
    var data = {grade: grade, overall: overall, time: time, sorttype: sorttype, sortorder: sortorder, operation: operation};
    $.get(url, data, function (reg) {
        var str = '';
        //解析打印数据
        var obj = eval("(" + reg + ")");
        //去除旧的数据节点
        $(".pbox_con table tbody").empty();
        //循环准备渲染新数据节点字符串
        for (var i = 0; i < obj.length; i++) {
            var first_unit = (obj[i]['start_deadline_unit'] == obj[i]['end_deadline_unit']) ? '' : obj[i]['start_deadline_unit'];
            first_unit = obj[i]['start_deadline_unit'];
            var inverst_num = (obj[i]['invest_num'] == 0) ? "待发布" : obj[i]['invest_num'] + "个";
            str += '<tr><td><a href="http://www.touzhijia.com/platform/details/' + obj[i]['plat_id'] + '">' + obj[i]['plat_cn_name'] + '</a></td><td style="width:100px;"><div class="td5-p"><span class="grade grade' + obj[i]['credit_level'] + '">' + obj[i]['credit_level'] + '</span><ul class="th-icon-ul"><li><span class="sx">资本充足：</span><span class="sz">' + obj[i]['levers'] + '</span></li><li><span class="sx">分散度：</span><span class="sz">' + obj[i]['fensandu'] + '</span></li><li><span class="sx">透明度：</span><span class="sz">' + obj[i]['toumingdu'] + '</span></li><li><span class="sx">流动性：</span><span class="sz">' + obj[i]['liudongxing'] + '</span></li><li><span class="sx">运营能力：</span><span class="sz">' + obj[i]['yunyingnengli'] + '</span></li><li><span class="sx">违约成本：</span><span class="sz">' + obj[i]['weiyuechengben'] + '</span></li></ul></div></td><td>' + obj[i]['min_rate'] + '% ~ ' + obj[i]['max_rate'] + '%</td><td>' + obj[i]['start_deadline'] + first_unit + '~' + obj[i]['end_deadline'] + obj[i]['end_deadline_unit'] + '</td><td>' + inverst_num + '</td><td><a class="btn btn_blue" href="http://www.touzhijia.com/platform/details/' + obj[i]['plat_id'] + '" ><span>查 看</span></a></td></tr>';
        }
        $(".pbox_con table tbody").html(str);
    });
}
/**
 * Created by py on 12/11/14.
 */
