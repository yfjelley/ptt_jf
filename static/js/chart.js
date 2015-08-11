$(function () {
    var data = [];
    var x_time = [];
    var y_number = [];
    var json_money = document.getElementById('json_money').value;
    var json_mount = document.getElementById('json_mount').value;
    var json_day = document.getElementById('json_day').value;
    var moneyList=eval("("+json_money+")")
    var numberList = eval("("+json_mount+")")
    var dayList = eval("("+json_day+")")
    for(var i=0;i<moneyList.length;i++) {
        for(var key in moneyList[i]){
            data[i]=parseInt(moneyList[i][key])/10000
        }
    };
    for(var i=0;i<numberList.length;i++) {
        for(var key in numberList[i]){
            y_number[i]=parseInt(numberList[i][key])
        }
    };
    for(var i=0;i<dayList.length;i++) {
        for(var key in dayList[i]){
            x_time[i]=dayList[i][key]
        }
    };
    var masterChart,
        detailChart;
    //获取当前时间
	var myDate = new Date();
	var nowyear = myDate.getFullYear();   //获取完整的年份(4位,1970-????)
	var nowmonth = myDate.getMonth();     //获取当前月份(0-11,0代表1月)
	var nowday = myDate.getDate();        //获取当前日(1-31)
    var number =  Math.round((x_time.length)/8);
    //获取交易额
     $('#container2').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '<b>平台每天交易额度</b>',
             style: {
                fontSize: '24px',

            }
        },

        xAxis: {
            tickInterval: number,
            categories: x_time
        },
        yAxis: {
//            max:20000, // 定义Y轴 最大值
            min: 0,
//            tickInterval:2000, // 刻度值
            labels: {
                formatter: function() {
                    return this.value ;
                },
            maxZoom: 0.1,
            x:0//调节x偏移
//                 y:-35,//调节y偏移
//                 rotation:25//调节倾斜角度偏移
            },
            title: {
                text: '投资额度(万)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}万元</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: '投资额度',
            data: data
        }]
    });
    //获取人数
    $('#container1').highcharts({
        chart: {

        },
        title: {
            text: '<b>平台每天交易人数</b>',
            style: {
                fontSize: '24px',

            }
        },
        xAxis: {
            tickInterval: number,
            categories: x_time
        },
        yAxis: {
//            max:20000, // 定义Y轴 最大值
            min: 0,
//            tickInterval:2000, // 刻度值
            labels: {
                formatter: function() {
                    return this.value ;
                },
            maxZoom: 0.1,
            x:0//调节x偏移
//                 y:-35,//调节y偏移
//                 rotation:25//调节倾斜角度偏移
            },
            title: {
                text: '投资人数'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}人</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: '投资人数',
            data: y_number

        }]
    });
});
