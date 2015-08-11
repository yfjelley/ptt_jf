/*免费获取时间的js代码*/
var secs = 60; 
var wait = secs * 1000; 
var update = function(num,value){ 
if (num == (wait/1000)){ 
 $("#rulesubmit").val("免费获取"); 
} 
else{ 
printnr = (wait/1000) - num; 
$("#rulesubmit").val("免费获取"); 
document.getElementById("div3").innerHTML=printnr;
} 
}; 
var timer = function(){ 
$("#rulesubmit").attr("disabled",false); 
$("#rulesubmit").val("免费获取"); 
}; 
$(function(){ 
(function(){ 
function getValidateCode(){ 
$("#rulesubmit").val("免费获取");
document.getElementById("div3").innerHTML=secs;
$("#rulesubmit").attr("disabled",true); 
for (i = 1; i <= secs;i++){ 
window.setTimeout("update(" + i + ")",i*1000); 
} 
window.setTimeout("timer()",wait); 
} 
$("#rulesubmit").click(function(){ 
getValidateCode();

}); 
})();
/*注意，我这里在测试的时候改成里匿名函数，其实不必这样做也可以实现 
getValidateCode()当作一个单独的函数，在$(function(){//点击按钮执行函数，即上面蓝色部分代码;});*/ 
}); 