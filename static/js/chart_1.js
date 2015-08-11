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
    $(document).ready(function() {
        // create the master chart
        function createMaster() {
            masterChart = $('#master-container').highcharts({
                chart: {
                    reflow: false,
                    borderWidth: 0,
                    backgroundColor: null,
                    marginLeft: 52,
                    marginRight: 18,
                    zoomType: 'x',
                    events: {

                        // listen to the selection event on the master chart to update the
                        // extremes of the detail chart
                        selection: function(event) {
                            var extremesObject = event.xAxis[0],
                                min = extremesObject.min,
                                max = extremesObject.max,
                                detailData = [],
                                xAxis = this.xAxis[0];

                            // reverse engineer the last part of the data
                            jQuery.each(this.series[0].data, function(i, point) {
                                if (point.x > min && point.x < max) {
                                    detailData.push({
                                        x: point.x,
                                        y: point.y
                                    });
                                }
                            });

                            // move the plot bands to reflect the new detail span
                            xAxis.removePlotBand('mask-before');
                            xAxis.addPlotBand({
                                id: 'mask-before',
                                from: Date.UTC(2014, 11, 25),
                                to: min,
                                color: 'rgba(0, 0, 0, 0.2)'
                            });

                            xAxis.removePlotBand('mask-after');
                            xAxis.addPlotBand({
                                id: 'mask-after',
                                from: max,
                                to: Date.UTC(nowyear, nowmonth, nowday-1),
                                color: 'rgba(0, 0, 0, 0.2)'
                            });


                            detailChart.series[0].setData(detailData);

                            return false;
                        }
                    }
                },
                title: {
                    text: null
                },
                xAxis: {
                    type: 'datetime',
                    showLastTickLabel: true,
                    labels: {
                        formatter: function () {
                            return Highcharts.dateFormat('%Y-%m-%d', this.value);
                        }
                    },

                    plotBands: [{
                        id: 'mask-before',
                        from: Date.UTC(2014, 11, 25),
                        to: Date.UTC(2014, 11, 28),
                        color: 'rgba(0, 0, 0, 0.2)'
                    }],
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    gridLineWidth: 0,
                    labels: {
                        enabled: false
                    },
                    title: {
                        text: null
                    },
                    min: 0.6,
                    showFirstLabel: false
                },
                tooltip: {
                    formatter: function() {
                        return false;
                    }
                },
                legend: {
                    enabled: false
                },
                credits: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        fillColor: {
                            linearGradient: [0, 0, 0, 70],
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, 'rgba(255,255,255,0)']
                            ]
                        },
                        lineWidth: 1,
                        marker: {
                            enabled: false
                        },
                        shadow: false,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        enableMouseTracking: false
                    }
                },

                series: [{
                    type: 'area',
                    name: 'USD to EUR',
                    pointInterval: 24 * 3600 * 1000,
                    pointStart: Date.UTC(2014, 11, 25),
                    data: data
                }],

                exporting: {
                    enabled: false
                }

            }, function(masterChart) {
                createDetail(masterChart)
            })
            .highcharts(); // return chart instance
        }

        // create the detail chart
        function createDetail(masterChart) {

            // prepare the detail chart
            var detailData = [],
                detailStart = Date.UTC(2014, 11, 28);

            jQuery.each(masterChart.series[0].data, function(i, point) {
                if (point.x >= detailStart) {
                    detailData.push(point.y);
                }
            });

            // create a detail chart referenced by a global variable
            detailChart = $('#detail-container').highcharts({
                chart: {
                    type: 'column',
                    marginBottom: 120,
                    reflow: false,
                    marginLeft: 40,
                    marginRight: 20,
                    style: {
                        position: 'absolute'
                    }
                },
                credits: {
                    enabled: false
                },
                title: {
                    text: '平台每天成交量(万元)'
                },

                xAxis: {
                    type: 'datetime',
                    labels: {
                        formatter: function () {
                            return Highcharts.dateFormat('%Y-%m-%d', this.value);
                        }
                    }
                },
                yAxis: {
                    title: {
                        text: ''
                    },
                    labels: {
                        formatter: function() {
                            return this.value ;
                        },
                        x:0
                    },
//                    max:10000, // 定义Y轴 最大值
                    min: 0,
//                    tickInterval:2000,  //刻度值
                    maxZoom: 0.1
                        },

                tooltip: {
                    formatter: function() {
                        var point = this.points[0];
                        return '<b>'+ point.series.name +'</b><br/>'+
                            Highcharts.dateFormat('%Y-%m-%d', this.x) + ':<br/>'+
                            '成交量:'+ Highcharts.numberFormat(point.y, 2)+'万元';
                    },
                    shared: true
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        marker: {
                            enabled: false,
                            states: {
                                hover: {
                                    enabled: true,
                                    radius: 3
                                }
                            }
                        }
                    }
                },
                series: [{
                    name: '每天成交额度',
                    pointStart: detailStart,
                    pointInterval: 24 * 3600 * 1000,
                    data: detailData
                }],

                exporting: {
                    enabled: false
                }

            }).highcharts(); // return chart
        }

        // make the container smaller and add a second container for the master chart
        var $container = $('#container')
            .css('position', 'relative');

        var $detailContainer = $('<div id="detail-container">')
            .appendTo($container);

        var $masterContainer = $('<div id="master-container">')
            .css({ position: 'absolute', top: 294, height: 70, width: '100%' })
            .appendTo($container);

        // create master and in its callback, create the detail chart
        createMaster();
    });
    //获取人数
    $('#container1').highcharts({
        chart: {

        },
        title: {
            text: '平台每天交易人数'
        },

        xAxis: {
            tickInterval: 5,
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
