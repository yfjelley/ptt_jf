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


/*字母随机的js*/

function only(ele,arr){ 
 if(arr.length==0){ 
  return true; 
 } 
 for(var j=0;j<arr.length;j++){ 
  if(ele==arr[j]){ 
   return false; 
  }else{ 
   return true; 
  } 
 } 
} 
  
var arr=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]; 
 
 function test(){
 	 	
 var randNum=null; 
 var old=[]; 
 var str=""; 
 function done(){ 
  randNum=Math.floor(Math.random()*26); 
  if(only(randNum,old)){ 
   str=str+arr[randNum]; 
   old.push(randNum); 
  } 
  else{ 
   done(); 
  } 
 } 
 for(var index=0;index<4;index++){ 
  done(); 
 }
document.getElementById("inp").value=str;

 }
 
$(function(){
	test();
})(arr)
$(function(){
  alert("xxxx");
  $("#rulesubmit").click(function(){
  var username = $("input[name=username]").val();
  $.post("/send_smscode/", {"phoneNum":username}, function(){});
})
})
