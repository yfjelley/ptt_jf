# coding=utf-8
import MySQLdb
from django.contrib import auth
from DjangoCaptcha import Captcha
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from searcher.forms import TRegForm, WXLoginForm, WXRegisterForm
from searcher.models import ThirdLogin, WXAccessToken
from searcher.models import UserInformation
from searcher.inner_views import user_auth, refresh_header
from django.core.urlresolvers import reverse
import httplib
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
import hashlib
from django.utils.encoding import smart_str
from xml.etree import ElementTree as etree
import sys
from models import UserReminder, Bid, BidHis, RemindQueue
from time import ctime, sleep
import datetime
import calendar
import threading
import time
__author__ = 'laven'

# the following two line is use for recieving chinese string from wechat server
reload(sys)
sys.setdefaultencoding('utf8')

def qq_is_first(request):
    resp = 0
    if request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        u_ajax = request.POST.get('name', None)
        if u_ajax:
            response['Content-Type'] = "application/json"
            r_u = request.POST.get('param', None)
            u = User.objects.filter(username=r_u)
            if u.exists():
                response.write('{"info": "用户已存在","status": "n"}')  # 用户已存在
                return response
            else:
                response.write('{"info": "用户可以使用","status": "y"}')
                return response
        openid = request.POST.get('openid', '')
        accesstoken = request.POST.get('accessToken', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        nickname = request.POST.get('nickname', '')
        url = request.POST.get('url', '')
        if openid != "" and accesstoken != "" and username == "" and email == "":
            tl = ThirdLogin.objects.filter(openId=openid)
            if tl.exists():
                if tl[0].qqFlag == "1":
                    u = User.objects.filter(id=(UserInformation.objects.filter(id=tl[0].userInfo_id)[0].user_id))
                    username = u[0].username
                    resp = 1
                else:
                    resp = 0
            else:
                resp = 0
        elif username != "" and email != "" and openid != "" and accesstoken != "":
            u = User.objects.filter(username=username)
            if u.exists():
                resp = 2
            else:
                new_user = User.objects.create_user(username=username, password="openid", email=email)
                new_user.save()
                u = UserInformation(user=new_user, photo_url=url)
                u.save()
                tl = ThirdLogin(openId=openid, accessToken=accesstoken, qqFlag=0)
                tl.userInfo = u
                tl.qqFlag = 1
                tl.save()
                resp = 1
        else:
            print "qq something unhopeful happend!"

        if resp == 1:
            user = User.objects.get(username=username)
            user.is_active = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            if user is not None and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = ''
            if resp == 2:
                error = "please input correctly!"
            form = TRegForm({'username': nickname, 'openid': openid, 'accessToken': accesstoken, 'url': url})
            return render_to_response("register.html", {'form': form, 'error': error, 'openid': openid}, context_instance=RequestContext(request))
    else:
        print "qq something unhopeful happend2!"
        # nickname = 'testqq'
        # openid = 'testqq_openid'
        # accesstoken = 'testqq_accessToken'
        # url = 'testqq_url'
        # form = TRegForm({'username': nickname, 'openid': openid, 'accessToken': accesstoken, 'url': url})
        # return render_to_response("register.html", {'form': form, 'openid': openid}, context_instance=RequestContext(request))

def wb_is_first(request):
    resp = 0
    if request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        wbid = request.POST.get('wbid', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        nickname = request.POST.get('nickname', '')
        url = request.POST.get('url', '')
        if wbid != "" and username == "" and email == "":
            tl = ThirdLogin.objects.filter(wbId=wbid)
            if tl.exists():
                if tl[0].wbFlag == "1":
                    u = User.objects.filter(id=(UserInformation.objects.filter(id=tl[0].userInfo_id)[0].user_id))
                    username = u[0].username
                    password = "wbid"
                    resp = 1
                else:
                    resp = 0
            else:
                resp = 0
        elif username != "" and email != "":
            u = User.objects.filter(username=username)
            if u.exists():
                resp = 2
            else:
                new_user = User.objects.create_user(username=username, password="wbid", email=email)
                new_user.save()
                u = UserInformation(user=new_user, photo_url=url)
                u.save()
                tl = ThirdLogin(wbId=wbid, wbFlag=0)
                tl.userInfo = u
                tl.wbFlag = 1
                tl.save()
                resp = 1
        else:
            print " wb something unhopeful happend!"

        if resp == 1:
            user = User.objects.get(username=username)
            user.is_active = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            if user is not None and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = ''
            if resp == 2:
                error = "please input correctly!"
            form = TRegForm({'username': nickname, 'wbid': wbid, 'url': url})
            return render_to_response("register.html", {'form': form, 'error': error, 'wbid': wbid}, context_instance=RequestContext(request))
    else:
        print " wb something unhopeful happend2!"
        # nickname = 'testwb'
        # wbid = 'testwb_id'
        # url = 'testwb_url'
        # form = TRegForm({'username': nickname, 'wbid': wbid, 'url': url})
        # return render_to_response("register.html", {'form': form}, context_instance=RequestContext(request))

def wx_is_first(request):
    resp = 0
    if request.method == 'GET':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        code = request.GET.get("code")
        data = initData(code)
        wxopenid = data['openid']
        wxaccesstoken = data['access_token']
        info = initInfo(wxopenid, wxaccesstoken)
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        nickname = info['nickname']
        url = info['headimgurl']
        if wxopenid != "" and wxaccesstoken != "" and username == "" and email == "":
            tl = ThirdLogin.objects.filter(wxopenId=wxopenid)
            if tl.exists():
                if tl[0].wxFlag == "1":
                    u = User.objects.filter(id=(UserInformation.objects.filter(id=tl[0].userInfo_id)[0].user_id))
                    username = u[0].username
                    resp = 1
                else:
                    resp = 0
            else:
                resp = 0
        else:
            print "wx something unhopeful happend!"

        if resp == 1:
            user = User.objects.get(username=username)
            user.is_active = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            if user is not None and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = ''
            if resp == 2:
                error = "please input correctly!"
            form = TRegForm({'username': nickname, 'openid': wxopenid, 'accessToken': wxaccesstoken, 'url': url})
            return render_to_response("register.html", {'form': form, 'error': error, 'wxopenid': wxopenid}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        wxopenid = request.POST.get('openid', '')
        wxaccesstoken = request.POST.get('accessToken', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        nickname = request.POST.get('nickname', '')
        url = request.POST.get('url', '')
        if username != "" and email != "" and wxopenid != "" and wxaccesstoken != "":
            u = User.objects.filter(username=username)
            if u.exists():
                resp = 2
            else:
                new_user = User.objects.create_user(username=username, password="wxopenid", email=email)
                new_user.save()
                u = UserInformation(user=new_user, photo_url=url)
                u.save()
                tl = ThirdLogin(wxopenId=wxopenid, wxaccessToken=wxaccesstoken, wxFlag=0)
                tl.userInfo = u
                tl.wxFlag = 1
                tl.save()
                resp = 1
        else:
            print "wx something unhopeful happend!"

        if resp == 1:
            user = User.objects.get(username=username)
            user.is_active = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            if user is not None and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = ''
            if resp == 2:
                error = "please input correctly!"
            form = TRegForm({'username': nickname, 'openid': wxopenid, 'accessToken': wxaccesstoken, 'url': url})
            return render_to_response("register.html", {'form': form, 'error': error, 'wxopenid': wxopenid}, context_instance=RequestContext(request))

    else:
        print "wx something unhopeful happend2!"

def initData(code):
    httpClient = None
    try:
        httpClient = httplib.HTTPSConnection('api.weixin.qq.com', timeout=30)
        httpClient.request('GET', '/sns/oauth2/access_token?appid=wx5705d3f981443fb8&secret=46f37dba35e5b57b5b98cc2437296f6b&code='+code+'&grant_type=authorization_code')
        response = httpClient.getresponse()
        if response.status == 200 and response.reason == 'OK':
            url = response.read()
            print "url:|||:", url
            time = json.loads(url)
        return time
    except Exception, e:
        print "httpClient to 'api.weixin.qq.com' initData get an error!", e
    finally:
        if httpClient:
            httpClient.close()

def initInfo(openid, access_token):
    httpClient = None
    try:
        httpClient = httplib.HTTPSConnection('api.weixin.qq.com', timeout=30)
        httpClient.request('GET', '/sns/userinfo?access_token='+access_token+'&openid='+openid)
        response = httpClient.getresponse()
        if response.status == 200 and response.reason == 'OK':
            url = response.read()
            print "url:|||:", url
            time = json.loads(url)
        return time
    except Exception, e:
        print "httpClient to 'api.weixin.qq.com' initInfo get an error!", e
    finally:
        if httpClient:
            httpClient.close()

def wxcheck(request):
    import logging
    logging.info("get request wxcheck!")
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request))
        return response
    else:
        logging.info("wechat push request content:" + request.body)
        try:
            xmlstr = smart_str(request.body)
            xml = etree.fromstring(xmlstr)
            ToUserName = xml.find('ToUserName').text
            FromUserName = xml.find('FromUserName').text
            CreateTime = xml.find('CreateTime').text
            MsgType = xml.find('MsgType').text
            reply_xml = "return_str"

            if MsgType == "event":
               Event = xml.find('Event').text
               if Event == "subscribe":
                   reply_xml = """<xml>
                   <ToUserName><![CDATA[%s]]></ToUserName>
                   <FromUserName><![CDATA[%s]]></FromUserName>
                   <CreateTime>%s</CreateTime>
                   <MsgType><![CDATA[text]]></MsgType>
                   <Content><![CDATA[%s]]></Content>
                   </xml>""" % (FromUserName, ToUserName, CreateTime,
                                "欢迎天天搜贷！为了您更好的使用我们的服务，请先绑定<a href='www.ddbid.com/wx_register?openid=%s'>创建</a>账号，谢谢！"%(FromUserName,FromUserName))

               elif Event == "TEMPLATESENDJOBFINISH":

                   msgId = xml.find('MsgID').text
                   logging.info("model message push callback!msgId:" + str(msgId))
                   status = xml.find('Status').text

                   if RemindQueue.objects.filter(messageId=msgId).exists():
                       logging.info("是否存在remindqueue里面的msgid")
                       rq = RemindQueue.objects.get(messageId=msgId)
                       if status == "success":
                            logging.info("success message call back in wxcheck")
                            rq.flag = 0
                            rq.save()
                       elif status == "failed:user block":
                            logging.info("userBlock message call back in wxcheck!")
                            tl = ThirdLogin.objects.filter(userInfo_id=rq.userId)
                            if tl.exists():
                                tl[0].wxBlock = 1
                                tl[0].save()
                   else:
                       logging.info("remind messageid not exsit!msgId:" + str(msgId))
                   reply_xml = """<xml>
                   <ToUserName><![CDATA[%s]]></ToUserName>
                   <FromUserName><![CDATA[%s]]></FromUserName>
                   <CreateTime>%s</CreateTime>
                   <MsgType><![CDATA[text]]></MsgType>
                   <Content><![CDATA[%s]]></Content>
                   </xml>""" % (FromUserName, ToUserName, CreateTime, "message callback confirm!")

            elif MsgType == "text":
               Content = xml.find('Content').text
               MsgId = xml.find('MsgId').text
               reply_xml = """<xml>
               <ToUserName><![CDATA[%s]]></ToUserName>
               <FromUserName><![CDATA[%s]]></FromUserName>
               <CreateTime>%s</CreateTime>
               <MsgType><![CDATA[text]]></MsgType>
               <Content><![CDATA[%s]]></Content>
               </xml>""" % (FromUserName, ToUserName, CreateTime, Content + "  Hello! this is a text message!")
            else:
               reply_xml = """<xml>
               <ToUserName><![CDATA[%s]]></ToUserName>
               <FromUserName><![CDATA[%s]]></FromUserName>
               <CreateTime>%s</CreateTime>
               <MsgType><![CDATA[text]]></MsgType>
               <Content><![CDATA[%s]]></Content>
               </xml>""" % (FromUserName, ToUserName, CreateTime, "Hello!")
            print "return :|||", reply_xml
            return HttpResponse(reply_xml)
        except Exception, e:
           print "chinese in request at wxcheck!", e
           return HttpResponse(e)




def checkSignature(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    #这里的token我放在setting，可以根据自己需求修改
    token = "999ddbid"
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None



def wx_binding(request):
    # print "get a request in wx_binding"
    # print "method is :"+request.method
    if request.method == 'POST':
        username = request.REQUEST.get('log_un', None)
        pwd = request.REQUEST.get('log_pwd', None)
        code = request.REQUEST.get('log_code', None)
        openid = request.REQUEST.get('openid', None)
        if username is None:
            form = WXLoginForm(request.POST)
            if form.is_valid():
                cd = form.clean()
                # username = cd['username']
                # pwd = cd['password']
                username = request.REQUEST.get('username', None)
                pwd = request.REQUEST.get('password', None)
                user = auth.authenticate(username=username, password=pwd)

                if user is None:
                    a = 2
                elif not user.is_active:
                    a = 3
                else:
                    auth.login(request, user)
                    a = 1
                if a == 1:
                    a = request.REQUEST.get('next', None)
                    if a:
                        return HttpResponseRedirect(a)
                    else:
                        u = UserInformation.objects.filter(user_id=User.objects.filter(username=username)[0].id)
                        tl = ThirdLogin.objects.filter(userInfo_id=u[0].id)
                        if tl.exists():
                            tl = ThirdLogin.objects.get(userInfo_id=u[0].id)
                            tl.wxopenId2 = openid
                            tl.save()
                        else:
                            tl = ThirdLogin(wxopenId2=openid, wxFlag2=0)
                            tl.userInfo = u[0]
                            tl.wxFlag2 = 1
                            tl.wxBlock = 0
                            tl.save()
                        return HttpResponseRedirect(reverse('searchindex'))
                else:
                    form.valiatetype(a)
                    return render_to_response('wx_login.html', {'form': form, 'openid': openid},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('wx_login.html', {'form': form, 'openid': openid},
                                          context_instance=RequestContext(request))

        return refresh_header(request, user_auth(request, username, pwd, code))
    else:
        form = WXLoginForm()
        next = request.GET.get('next', None)
        openid = request.GET.get('openid', None)
        return render_to_response('wx_login.html', {'form': form, 'next': next, 'openid': openid},
                                  context_instance=RequestContext(request))


def wx_register(request):
    if request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        openid = request.REQUEST.get('openid', None)
        u_ajax = request.POST.get('name', None)
        if u_ajax:
            response['Content-Type'] = "application/json"
            r_u = request.POST.get('param', None)
            u = User.objects.filter(username=r_u)
            if u.exists():
                response.write('{"info": "用户已存在","status": "n"}')  # 用户已存在
                return response
            else:
                response.write('{"info": "用户可以使用","status": "y"}')
                return response
        form = WXRegisterForm(request.POST)
        if form.is_valid():
            username = request.REQUEST.get('username', None)
            pwd1 = request.REQUEST.get('password', None)
            pwd2 = request.REQUEST.get('password2', None)
            em = request.REQUEST.get('email', None)
            flag = 0
            u = User.objects.filter(username=username)
            if u.exists():
                form.valiatetype(2)
                flag = 1
            if pwd1 != pwd2:
                form.valiatetype(3)
                flag = 1
            if flag == 1:
                return render_to_response("wx_reg.html", {'form': form, 'openid': openid}, context_instance=RequestContext(request))
            elif pwd1 == pwd2:
                new_user = User.objects.create_user(username=username, password=pwd1)
                new_user.save()
                u = UserInformation(user=new_user, photo_url='/static/upload/default.png', email=em, abcdefg=pwd1)
                u.save()
                user = auth.authenticate(username=username, password=pwd1)
                auth.login(request, user)
                u = UserInformation.objects.filter(user_id=User.objects.filter(username=username)[0].id)
                tl = ThirdLogin.objects.filter(userInfo_id=u[0].id)
                if tl.exists():
                    tl = ThirdLogin.objects.get(userInfo_id=u[0].id)
                    tl.wxopenId2 = openid
                    tl.save()
                else:
                    tl = ThirdLogin(wxopenId2=openid, wxFlag2=0)
                    tl.userInfo = u[0]
                    tl.wxFlag2 = 1
                    tl.wxBlock = 0
                    tl.save()
                #直接定向到首页
                return HttpResponseRedirect(reverse('searchindex'))
        else:
            return render_to_response("wx_reg.html", {'form': form, 'openid': openid}, context_instance=RequestContext(request))
    else:
        form = WXRegisterForm()
        openid = request.GET.get('openid', None)
        return render_to_response("wx_reg.html", {'form': form, 'openid': openid}, context_instance=RequestContext(request))

def ch_access_token(request):
    httpClient = None
    try:
        httpClient = httplib.HTTPSConnection('api.weixin.qq.com', timeout=30)
        httpClient.request('GET', '/cgi-bin/token?grant_type=client_credential&appid=wx90391d14181ccbdc&secret=221bdc228ef29d4abbc8e9a5534e10b1')
        response = httpClient.getresponse()
        if response.status == 200 and response.reason == 'OK':
            url = response.read()
            # print "url:|||:", url
            jsonz = json.loads(url)
            accessToken = jsonz['access_token']
            expiresIn = time.time() + int(jsonz['expires_in'])
            print accessToken, expiresIn
            at = WXAccessToken.objects.filter(id=1)
            if at.exists():
                at = WXAccessToken.objects.get(id=1)
                at.accessToken = accessToken
                at.expiresIn = expiresIn
                at.save()
            else:
                at = WXAccessToken(accessToken=accessToken, expiresIn=expiresIn)
                at.Flag = 1
                at.save()
        return HttpResponseRedirect("/")
    except Exception, e:
        print "httpsClient to 'api.weixin.qq.com' ch_access_token get an error!", e
    finally:
        if httpClient:
            httpClient.close()


def send_message(request):
    import logging
    logging.info("send_message function begain!")
    httpClient = None
    try:
        rq = RemindQueue.objects.filter(flag=1)
        subName = "标的名称"
        if rq.exists():
            for s in rq:
                modelId = "F7InOkwTYtD5KiN6PobTTyR1gs_Rz6OYEFeSJu_Jg4g"

                if s.type == '3':
                    remType = "还款提醒"
                    bidn = Bid.objects.filter(id=s.subjectId)

                    if bidn:
                        bidn = Bid.objects.get(id=s.subjectId)
                        subName = bidn.name
                    else:
                        bidn = BidHis.objects.get(id=s.subjectId)
                        subName = bidn.name
                elif s.type == '2':
                    remType = "结标提醒"
                    bidn = BidHis.objects.get(id=s.subjectId)
                    if bidn:
                        subName = bidn.name
                    else:
                        logging.error("结标提醒读取标的名称时没有读到数据:id:" + str(s.subjectId))
                elif s.type == '5':
                    remType = "余额提醒"
                    bidn = BidHis.objects.filter(id=s.subjectId)
                    if bidn:
                        bidn = BidHis.objects.get(id=s.subjectId)
                        subName = bidn.name
                    else:
                        logging.error("余额提醒读取标的名称时没有读到数据:id:" + str(s.subjectId))
                else:
                    remType = "不可能提醒的提醒"

                remCont = "您有一条新的标的名为'" + str(subName) + "'的信息提醒:"
                remTime = s.add_date
                tlo = ThirdLogin.objects.filter(userInfo_id=s.userId, wxBlock=0)
                uOpenId = ""
                if tlo.exists():
                    uOpenId = ThirdLogin.objects.get(userInfo_id=s.userId).wxopenId2

                # print "remType:", remType
                # print "remCont", remCont
                # print "remTime", remTime
                # print "modelId", modelId
                # print "subName", subName
                # print "uOpenId", uOpenId

                # uOpenId = "o-0DAjlKYCVOjTonFN-R5NZNuNNw"#test on my wechat message
                if uOpenId:
                    access_token = WXAccessToken.objects.get(id=1)
                    if access_token:
                        if access_token.expiresIn < time.time():
                            ch_access_token(request)
                    else:
                        ch_access_token(request)
                    access_token_str = access_token.accessToken

                    str1 = '''{
                               "touser": "''' + uOpenId + '''",
                               "template_id": "''' + modelId + '''",
                               "url": "http://ddbid.com/wx_bid_detail/'''+str(s.subjectId) + '''/",
                               "topcolor": "#FF0000",
                               "data":{
                                       "first":{
                                           "value":"''' + remCont + '''",
                                           "color":"#173177"
                                       },
                                       "keynote1":{
                                           "value":"''' + remType + '''",
                                           "color":"#173177"
                                       },
                                       "keynote2":{
                                           "value":"''' + str(remTime) + '''",
                                           "color":"#173177"
                                       },
                                       "remark":{
                                           "value":"了解更多请点击详情.",
                                           "color":"#173177"
                                       }
                               }
                           }'''
                    js = json.loads(str1)
                    headers = {"Content-type": "application/json; encoding=utf-8", "Accept": "text/plain"}
                    httpClient = httplib.HTTPSConnection("api.weixin.qq.com", timeout=30)
                    httpClient.request("POST", "/cgi-bin/message/template/send?access_token="+access_token_str, json.dumps(js), headers)
                    response = httpClient.getresponse()
                    # print response.status
                    # print response.reason
                    # print response.read()
                    # print response.getheaders() #获取头信息
                    jsov = response.read()
                    jso = json.loads(jsov)
                    if jso["errmsg"] == "ok":
                        logging.info("send a new message:" + str1)
                        s.messageId = jso["msgid"]
                        s.save()
                else:
                    logging.warning("用户不存在!remindqueue_id:" + str(s.id))
                    s.flag = 0
                    s.save()
    except Exception, e:
        logging.exception("开始执行结标提醒exception:" + str(e))
    finally:
        if httpClient:
            httpClient.close()
        global thread_control
        thread_control = 0

thread_control = 0

def remind_thread(request):
    import logging
    logging.info('all thread开始!')
    global thread_control
    if thread_control == 0:
        thread_control = 1
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        logging.info("all thread over")
        thread_control = 0
    return HttpResponseRedirect('/')

def test_thread_on(request):
    import logging
    logging.info('test thread on or not')
    global thread_control
    response = HttpResponse()
    response['Content-Type'] = "text"
    response.write(thread_control)
    return response

def remind1(func):
    while True:
        over_remind()
        balance_remind()
        request = ""
        send_message(request)
        sleep(10*60)

def remind2(func):
    while True:
        profit_remind()
        sleep(4*60*60)

threads = []
t1 = threading.Thread(target=remind1, args=(u'love sell',))
threads.append(t1)
t2 = threading.Thread(target=remind2, args=(u'afanda',))
threads.append(t2)

def over_remind():
    import logging
    try:
        logging.info("开始执行结标提醒!over_remind begain!")
        userReminders = UserReminder.objects.filter(is_reminded=0, status=1, reminder_id=2)
        for ur in userReminders:
            u = UserInformation.objects.filter(user_id=ur.user_id)
            if ur.value != 0 and u.__len__() > 0:
                bid = ur.bid_id
                subjectHis = BidHis.objects.filter(id=bid)
                if subjectHis.__len__() > 0:
                    remindQueue = RemindQueue(userId=u[0].id,
                                              subjectId=subjectHis[0].id,
                                              type=2,
                                              bEndDate=subjectHis[0].end_time,
                                              flag=1)
                    remindQueue.save()
                    logging.info("create a new remind data!")
                    ur.is_reminded = 1
                    ur.save()
            else:
                logging.warning("over_remind:invalid data or there is no user in database!userreminder_id:" + str(ur.id))

                ur.is_reminded = 1
                ur.save()
    except Exception, e:
        logging.exception("开始执行结标提醒exception:" + str(e))
    finally:
        global thread_control
        thread_control = 0
    return

def balance_remind():
    import logging
    logging.info("开始执行余标提醒!balance_remind begain!")
    try:
        userReminders = UserReminder.objects.filter(is_reminded=0, status=1, reminder_id=5)
        for ur in userReminders:
            u = UserInformation.objects.filter(user_id=ur.user_id)
            if ur.value != 0 and u.__len__() > 0:
                bid = ur.bid_id
                subject = Bid.objects.filter(id=bid)
                if subject.__len__() > 0:
                    balance = subject[0].amount * (100 - subject[0].process) / 100
                    if balance < ur.value:
                        remindQueue = RemindQueue.objects.create(userId=u[0].id,
                                                                 subjectId=subject[0].id,
                                                                 type=5,
                                                                 bEndDate=subject[0].end_time,
                                                                 limit=ur.value,
                                                                 flag=1)
                        remindQueue.save()
                        logging.info("create a new remind data!")
                        ur.is_reminded = 1
                        ur.save()
                    else:
                        logging.info("the balance is bigger than the value!")
                else:
                    logging.warning("there is no data in bid table(bid is done!). no balance remind. mark is_remind")
                    ur.is_reminded = 1
                    ur.save()
            else:
                logging.warning("balance_remind:invalid data or there is no user in database!userreminder_id:" + str(ur.id))
                ur.is_reminded = 1
                ur.save()
    except Exception, e:
        logging.exception("开始执行余标提醒exception:" + str(e))
    finally:
        global thread_control
        thread_control = 0

    return

def profit_remind():
    import logging
    try:
        logging.warning("开始执行收益提醒!profit_remind begain!")
        userReminders = UserReminder.objects.filter(is_reminded=0, status=1, reminder_id=3)
        logging.info("profit remind userreminder num:" + str(userReminders.__len__()))
        for ur in userReminders:
            u = UserInformation.objects.filter(user_id=ur.user_id)
            if ur.value != 0 and u.__len__() > 0:
                bid = ur.bid_id
                subjectHis = BidHis.objects.filter(id=bid)
                logging.info("bidhis:" + str(bid))
                if subjectHis.__len__() > 0:
                    ndate = subjectHis[0].end_time
                    if ndate:
                        logging.info("ndate:" + str(ndate))
                        now = datetime.datetime.now()
                        logging.info("datetime.datetime' and 'NoneType:" + str(now))
                        diffSeconds = (now-ndate).total_seconds()
                        term = subjectHis[0].term
                        x = term*30*24*60*60
                        if diffSeconds < x:
                            d = datetime.datetime.now()
                            year = d.year
                            month = d.month
                            if month == 1:
                                month = 12
                                year -= 1
                            else:
                                month -= 1
                            last_month_day = calendar.monthrange(year, month)[1]
                            if last_month_day < ur.value:
                                day2 = last_month_day
                            else:
                                day2 = ur.value
                            if day2 == time.localtime()[2]:
                                remindQueue = RemindQueue.objects.create(userId=u[0].id,
                                                                         subjectId=subjectHis[0].id,
                                                                         type=3,
                                                                         bEndDate=subjectHis[0].end_time,
                                                                         flag=1)
                                remindQueue.save()
                                logging.info("create a new remind data!")

                        else:
                            logging.info("the now is bigger than the enddata+term!userreminder_id" + str(bid))
                            ur.is_reminded = 1
                            ur.save()
                    else:
                        logging.info("there is no end time in bid_his table.user_remind_id:" + str(bid))
                        ur.is_reminded = 1
                        ur.save()
            else:
                logging.warning("profit_remind:invalid data or there is no user in database!userreminder_id:" + str(ur.id))
                ur.is_reminded = 1
                ur.save()
    except Exception, e:
        logging.exception("开始执行收益提醒exception:" + str(e))
    finally:
        global thread_control
        thread_control = 0
    return

def wx_bid_detail(request, objectid):
    try:
        b = Bid.objects.get(id=objectid)
    except ObjectDoesNotExist:
        b = BidHis.objects.get(id=objectid)
    now_date = datetime.datetime.now()
    yes_time_1 = now_date + datetime.timedelta(days=-1)
    connection = MySQLdb.connect(host="ddbid2015.mysql.rds.aliyuncs.com", user="django", passwd="ddbid_django1243", db="ddbid_db")
    cursor = connection.cursor()
    arr_money = []
    arr_mount = []
    arr_day = []
    if b.platform.id != 13:
        sql = "select day_id,amount,inv_quantity from t_platform_info_daily where platform_id=%d order by day_id" %(b.platform.id)
    else:
        sql = 'select day_id,amount,inv_quantity from t_platform_info_daily where platform_id=10 order by day_id'
    cursor.execute(sql)
    cds = cursor.fetchall()
    i = 0
    for abc in cds:
        i += 1

        money = {'money%d' % i: abc[1]}
        mount = {'amount%d' % i: abc[2]}
        day = {'day%d' % i: abc[0]}
        arr_money.append(money)
        arr_mount.append(mount)
        arr_day.append(day)

    json_money = json.dumps(arr_money, cls=DjangoJSONEncoder)
    json_mount = json.dumps(arr_mount, cls=DjangoJSONEncoder)
    json_day = json.dumps(arr_day, cls=DjangoJSONEncoder)
    cursor.close()
    return render_to_response("wx_bid_detail.html",
                              {'bid': b, 'json_money': json_money, 'json_mount': json_mount, 'json_day': json_day},
                              context_instance=RequestContext(request))

