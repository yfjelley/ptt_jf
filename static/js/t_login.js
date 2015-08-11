QC.Login({
  btnId : "qqLoginBtn",//插入按钮的html标签id
  size : "C_S",//按钮尺寸
  scope : "get_user_info",//展示授权，全部可用授权可填 all
  display : "pc"//应用场景，可选
 }, function(reqData, opts){
     //alert("login success：" + QC.Login.check());
     //判断登陆是否成功
     if (QC.Login.check()){
         //拿取平台openid
         QC.Login.getMe(function(openId, accessToken){
             //alert("拿到的openid：" + openId + " accessToken:" + accessToken);
             //判断是否为首次登陆
             $.post("{% url 'qq_is_first' %}",
                {
                    openid: openId,
                    accessToken: accessToken
                },
                function (data) {
                    alert(data);
                    window.document.write(data);
                },"html");
         });
     }else{
         alert("login failed! please try again!");
     }
   }, function(opts){//注销成功
         alert('QQ登录 注销成功');
   });