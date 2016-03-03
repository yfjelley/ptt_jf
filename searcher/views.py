# coding=utf-8
#from __future__ import unicode_literals
import MySQLdb
import datetime
from itertools import chain
import json
import os
import random
from searcher.task import sendmail
from django.core.serializers.json import DjangoJSONEncoder
from DjangoCaptcha import Captcha
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from PIL import Image
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from ddbid.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from searcher.forms import ContactForm, SearchForm, LoginForm, UserInformationForm, RegisterForm, ForgetPWForm, ModfiyPWForm, PublishForm,ModfiyPForm
from searcher.inner_views import index_loading, data_filter, result_sort, get_pageset, get_user_filter, user_auth, \
    refresh_header,send_flow_all,user_get_ip
from searcher.models import Bid, UserFavorite, Platform, UserInformation, DimensionChoice, UserFilter, UserReminder, \
    WeekHotSpot, BidHis, ReminderUnit, About_us, Partners, Frendlink, Project,project_forum,Signal,MediaReports,invest_detail,Extend
from ddbid import conf
from django.db.models import Q
import simplejson


from searcher.models import RegistrationAgreement


__author__ = 'pony'

storage = FileSystemStorage(
    location=conf.UPLOAD_PATH,
    base_url='/static/upload/'
)

dict_code = {}

def login(request):
    if request.method == 'POST':
        username = request.REQUEST.get('log_un', None)
        pwd = request.REQUEST.get('log_pwd', None)
        code = request.REQUEST.get('log_code', None)
        if username is None:
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.clean()
                username = cd['username']
                pwd = cd['password']
                code = cd['vcode']
                i = user_auth(request, username, pwd, code)
                if i == 1:
                    a = request.REQUEST.get('next', None)
                    if a:
                        return HttpResponseRedirect(a)
                    else:
                        user = User.objects.get(username=username)
                        login_times = user.userinformation.login_times
                        if login_times:
                            user.userinformation.login_times = int(login_times) +1
                        else:
                            user.userinformation.login_times  = 1
                        user.userinformation.save()
                        return HttpResponseRedirect(reverse('index_jf'))
                else:
                    form.valiatetype(i)
                    return render_to_response('login.html', {'form': form, },
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('login.html', {'form': form, },
                                          context_instance=RequestContext(request))

        return refresh_header(request, user_auth(request, username, pwd, code))
    else:
        form = LoginForm()
        next = request.GET.get('next', None)
        return render_to_response('login.html', {'form': form, 'next': next},
                                  context_instance=RequestContext(request))

def forgetpw(request):
    if request.method == 'POST':
        form = ForgetPWForm(request.POST)
        if form.is_valid():
            cd = form.clean()
            username = cd['username']
            _code = request.session.get('sms_code')
            smscode = cd['smscode']
            user = User.objects.get(username=username)
            pw = user.userinformation.abcdefg


            if pw is not None and _code == int(smscode):
                user = auth.authenticate(username=username, password=pw)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    #return HttpResponse(u'登录成功')
                    return HttpResponseRedirect(reverse('index_jf'))
                else:
                    return HttpResponse(u'输入错误')
                    #return render_to_response('forgetpwd.html',{"form":form},
                      #                context_instance=RequestContext(request))

            else:
                form.valiatetype(2)
                return render_to_response('forgetpwd.html',{"form":form},
                                      context_instance=RequestContext(request))

        else:
            return render_to_response('forgetpwd.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = ForgetPWForm()
        return render_to_response('forgetpwd.html', {'form': form}, context_instance=RequestContext(request))

def verifycode(request):
    figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ca = Captcha(request)
    ca.words = [''.join([str(random.sample(figures, 1)[0]) for i in range(0, 4)])]
    ca.type = 'word'
    ca.img_width = 60
    ca.img_height = 28
    return ca.display()

def checkvcode(request):
    if_vcode = request.POST.get('name', None)
    _code = request.session.get('_django_captcha_key')
    if if_vcode:
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        vcode = request.POST.get('param', None)
        if _code.lower() == vcode.lower() :
            response.write('{"info": "","status": "y"}')
            return response
        else:
            response.write('{"info": "验证码错误","status": "n"}')
            return response

def checksmscode(request):
    if_smscode = request.POST.get('name', None)
    _code = request.session.get("sms_code")
    if if_smscode:
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        smscode = request.POST.get('param', None)
        if _code  == int(smscode) :
            response.write('{"info": "","status": "y"}')
            return response
        else:
            response.write('{"info": "验证码错误","status": "n"}')
            return response

def checkuser(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    u_ajax = request.POST.get('name', None)
    if u_ajax:
        response['Content-Type'] = "application/json"
        r_u = request.POST.get('param', None)
        u = User.objects.filter(username=r_u)
        if u.exists():
            response.write('{"info": "","status": "y"}')
            return response
        else:
            response.write('{"info": "用户不存在","status": "n"}')  # 用户不存在
            return response
def checkuser_phone(request):
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

                response.write('{"info": "","status": "y"}')
                return response

def register(request):
    print request
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
        form = RegisterForm(request.POST)


        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            pwd1 = cd['password']
            pwd2 = cd['password2']

            smscode = cd['smscode']
            code = cd['vcode']
            registration_invitation_code = cd['extend']
            ca = Captcha(request)
            flag = 0
            u = User.objects.filter(username=username)
            f = ca.check(code)
            if u.exists():
                form.valiatetype(2)
                flag = 1
            if pwd1 != pwd2:
                form.valiatetype(3)
                flag = 1
            if not f:
                form.valiatetype(4)
                flag = 1
            if flag == 1:
                return render_to_response("reg.html", {'form': form}, context_instance=RequestContext(request))
            elif pwd1 == pwd2 and f:
                new_user = User.objects.create_user(username=username, password=pwd1)
                new_user.save()
                # initial={'photo_url': '/static/upload/default.png'}
                u = UserInformation(user=new_user, photo_url='/static/upload/default.png', abcdefg=pwd1,cellphone=username)
                u.save()

                for i in range(1,10):
                    code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(6)))
                    exist = Extend.objects.filter(extend_code=code)
                    if not exist:
                        e = Extend(extend_code=code,extend_user=new_user, regist_code=registration_invitation_code)
                        e.save()
                        break

                user = auth.authenticate(username=username, password=pwd1)
                auth.login(request, user)
                send_flow_all(username)
                p = re.compile('^13[4-9][0-9]{8}|^15[0,1,2,7,8,9][0-9]{8}|^18[2,7,8][0-9]{8}|^147[0-9]{8}|^178[0-9]{8}')
                p1 = re.compile('^18[0,1,9][0-9]{8}|^133[0-9]{8}|^153[0-9]{8}|^177[0-9]{8}')
                phone = username
                if p.match(str(phone)):
                    flag1 = 1
                elif p1.match(str(phone)):
                    flag1 = 2
                else:
                    flag1 = 3
                return HttpResponseRedirect(reverse('index_jf'))
                #return  render_to_response("reg_success.html", {'flag1':flag1}, context_instance=RequestContext(request))
        else:
            return render_to_response("signup.html", {'form': form}, context_instance=RequestContext(request))
    else:
        code = request.GET.get('code',None)
        print code
        form = RegisterForm()
        return render_to_response("signup.html", {'form': form,'code':code}, context_instance=RequestContext(request))


@login_required
def logout(request):
    """

    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('index_jf'))

@login_required
def myfavorite(request, tid):
    flag = int(tid)
    favorites = {}
    userid = auth.get_user(request).id
    userfavoriteBid = UserFavorite.objects.filter(user=userid, favorite_type=1).values("favorite_id")
    userfavoriteplatform = UserFavorite.objects.filter(user=userid, favorite_type=2).values("favorite_id")
    favoriteBidNow = Bid.objects.filter(id__in=userfavoriteBid)
    favoriteBidHis = BidHis.objects.filter(id__in=userfavoriteBid)
    favoriteplatform = Platform.objects.filter(id__in=userfavoriteplatform)
    if flag == 4:
        favorites = list(chain(favoriteBidNow, favoriteBidHis))
    else:
        favorites = favoriteplatform
    return render_to_response("user_favorite.html",
                              {'favorites': favorites, 'flag': flag}, context_instance=RequestContext(request))



def auth_register(request):
    u = UserInformation.objects.get(user=request.user)

    u.business_card = request.POST.get('icard')
    u.realname = request.POST.get('real_name')
    u.authentication_class = int(request.POST.get('type'))+1
    u.invest_class = 2
    u.save()
    return HttpResponse()


@login_required
def userinfo(request,objectid=None):
    url = None
    user = auth.get_user(request)
    flag = 1
    if request.method == 'POST':
        print "xxxx"
        form  = UserInformationForm(request.POST)
        print form
        f = request.FILES.get('file',None)
        print f
        if f:
            print "xwwwwx"
            extension = os.path.splitext(f.name)[-1]
            msg = None
            if f.size > 1048576:
                msg = u"图片大小不能超过1MB"
            if (extension not in ['.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF']) or ('image' not in f.content_type):
                msg = u"图片格式必须为jpg，png，gif"
            if msg:
                return render_to_response("userinfo.html", {'form': form,'error': msg},
                                          context_instance=RequestContext(request))

            im = Image.open(f)
            im.thumbnail((120, 120))
            name = 'p_user' + storage.get_available_name(str(user.id)) + '.png'
            print name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            print url
        if form.is_valid():
            try:
                u_i = UserInformation.objects.get(user=user)
                form1 = UserInformationForm(request.POST, instance=u_i)
                u_i = form1.save(commit=False)
                if url:
                    u_i.photo_url = url
            except ObjectDoesNotExist:
                u_i = form.save(commit=False)
                u_i.user = user
                u_i.photo_url = url
            u_i.save()
        else:
            return render_to_response("userinfo.html", {'form': form, 'flag': flag},
                                      context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('userinfo'))
    else:
        try:
            form = UserInformationForm(instance=user.userinformation)
        except ObjectDoesNotExist:
            form = UserInformationForm()
        #领投项目

        leader  = invest_detail.objects.filter(invest_user=request.user)

        #跟投项目
        invest = Project.objects.filter(investor=request.user)

        #我发布的项目
        publish_pr = Project.objects.filter(publish=user)
        #我关注的项目
        attention_pr =   Project.objects.filter(click=user)
        #我关注的人
        u = User.objects.get(username=request.user)

        attention_persion = u.userinformation.attention_persion.all()

        signal =  Signal.objects.filter(who=request.user).order_by("-add_date")[0:6]
        notice = Signal.objects.filter(type=0).order_by("-add_date")[0:6]

        extend = Extend.objects.filter(extend_user=request.user)
        if extend:
            extend = extend[0]
        print extend

    return render_to_response("userinfo.html", {"extend":extend,"notice":notice,"signal":signal,'form': form,"leader":leader,"invest":invest,\
                                                "publish_pr":publish_pr,"attention_pr":attention_pr,"attention_persion":attention_persion},
                              context_instance=RequestContext(request))
def generate(request):
    for i in range(1,10):
        code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(6)))
        exist = Extend.objects.filter(extend_code=code)
        if not exist:
            e = Extend(extend_code=code,extend_user=request.user)
            e.save()
            break
    return HttpResponse()

def contact_us(request):
    return render_to_response('contact_us.html', context_instance=RequestContext(request))

def disclaimer(request):
    return render_to_response('disclaimer.html', context_instance=RequestContext(request))

def phone_infoPage(request):
    return render_to_response('test_phone.html', context_instance=RequestContext(request))


import urllib2, urllib, hashlib, random,re
def send_smscode(request):
    if request.user.is_authenticated():
        key = "limit_visit:" + send_smscode.__name__ +':'+ str(request.user.id)
    else:
        key = "limit_visit:" + send_smscode.__name__ +':'+ str(user_get_ip(request))
    failed_num = cache.get(key,0)
    print "failed_num",failed_num
    if failed_num >= 10:
        return HttpResponse(u"您的短信次数超个10次，请24小时后再试！")

    failed_num += 1
    cache.set(key, failed_num, 24*60*60)

    phoneNum = request.POST.get('phoneNum', '')
    p=re.compile('^1200[0-9]{7}$')
    a=p.match(phoneNum)
    if a:
        return HttpResponse()
    else:
        m = hashlib.md5()
        m.update('shcdjr2')
        random_code = random.randint(1000, 9999)
        request.session["sms_code"] = random_code
        content = "您的验证码是：%s，有效期为五分钟。如非本人操作，可以不用理会!"%random_code
        print content
        data = """
                  <Group Login_Name ="%s" Login_Pwd="%s" OpKind="0" InterFaceID="" SerType="xxxx">
                  <E_Time></E_Time>
                  <Item>
                  <Task>
                  <Recive_Phone_Number>%d</Recive_Phone_Number>
                  <Content><![CDATA[%s]]></Content>
                  <Search_ID>111</Search_ID>
                  </Task>
                  </Item>
                  </Group>
               """ % ("shcdjr2", m.hexdigest().upper(), int(phoneNum), content.decode("utf-8").encode("GBK"))

        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        request = urllib2.Request(
                                   url = r'http://userinterface.vcomcn.com/Opration.aspx',
                                   headers= {'Content-Type':'text/xml'},
                                   data = data
                                  )
        print opener.open(request).read()
        return HttpResponse()


def send_smscode_modify(request):
    if request.user.is_authenticated():
        key = "limit_visit:" + send_smscode_modify.__name__ +':'+ str(request.user.id)
    else:
        key = "limit_visit:" + send_smscode_modify.__name__ +':'+ str(user_get_ip(request))
    failed_num = cache.get(key,0)
    if failed_num >= 2:
        return HttpResponse(u"您修改账号次数超个2次，请30天后再试！")

    failed_num += 1
    cache.set(key, failed_num, 30*24*60*60)

    phoneNum = request.POST.get('phoneNum', '')
    p=re.compile('^1200[0-9]{7}$')
    a = p.match(phoneNum)
    if a:
        return HttpResponse()
    else:
        user = User.objects.filter(username=int(phoneNum))
        print user
        if not len(user):
            print "ceshi"
            m = hashlib.md5()
            m.update('shcdjr2')
            random_code = random.randint(1000, 9999)
            request.session["sms_code"] = random_code
            content = "您的验证码是：%s，有效期为五分钟。如非本人操作，可以不用理会!"%random_code
            print content
            data = """
                      <Group Login_Name ="%s" Login_Pwd="%s" OpKind="0" InterFaceID="" SerType="xxxx">
                      <E_Time></E_Time>
                      <Item>
                      <Task>
                      <Recive_Phone_Number>%d</Recive_Phone_Number>
                      <Content><![CDATA[%s]]></Content>
                      <Search_ID>111</Search_ID>
                      </Task>
                      </Item>
                      </Group>
                   """ % ("shcdjr2", m.hexdigest().upper(), int(phoneNum), content.decode("utf-8").encode("GBK"))
            print "1"
            cookies = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookies)
            print "3"
            request = urllib2.Request(
                                       url = r'http://userinterface.vcomcn.com/Opration.aspx',
                                       headers= {'Content-Type':'text/xml'},
                                       data = data
                                      )
            print "4"
            print opener.open(request).read()
        return HttpResponse()
def agreement(request):
    ag = RegistrationAgreement.objects.filter(name="registration_agreement")
    return render_to_response('agreement.html',{'agreement':ag[0].agreement}, context_instance=RequestContext(request))


def index_zc(request):
    #1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例
    pr = Project.objects.all().distinct()
    for i in pr:
        f = invest_detail.objects.filter(invest_project=i)
        m = 0
        for j in f:
            m += float(j.invest_num)
        i.finish = int(m)
        i.save()

    return render_to_response('newindex_page.html',{"project":pr},context_instance=RequestContext(request))



def safecenter(request):
    #print "safecenter:", request
    if request.method =="POST":
        form = ModfiyPWForm(request.POST)
        if form.is_valid():
            print "form is valid"
            username = request.user.username
            print username

            user = User.objects.get(username=username)
            pw = user.userinformation.abcdefg
            print  pw,user

            cd = form.cleaned_data
            password = cd['password']
            password2 = cd['password2']
            print "xxxxxxxxxxxxxxxx"
            if int(password) == int(password2) :
                user = auth.authenticate(username=username, password=pw)
                if user is not None and user.is_active:
                    user.set_password(password)
                    user.save()
                    user.userinformation.abcdefg = password
                    user.userinformation.save()
                    t = get_template('success.html')
                    content_html = t.render(
                            RequestContext(request,{'form':form,'status':u'密码修改成功！'}))

                    payload = {
                            'content_html': content_html,
                            'success': True,
                        }
                    return HttpResponse(json.dumps(payload), content_type="application/json")

            else:
                print "is not valid"
                t = get_template('success.html')
                content_html = t.render(
                        RequestContext(request,{'form':form,'status':u'两次输入密码不一致'}))

                payload = {
                        'content_html': content_html,
                        'success': True,
                    }
                return HttpResponse(json.dumps(payload), content_type="application/json")
        else:

            t = get_template('success.html')
            content_html = t.render(
                    RequestContext(request,{'form':form,'status':u'输入非法！'}))

            payload = {
                    'content_html': content_html,
                    'success': True,
                }
            return HttpResponse(json.dumps(payload), content_type="application/json")

    else:
        print "safecenter"
        form = ModfiyPWForm()
        t = get_template('safecenter.html')
        content_html = t.render(
                RequestContext(request,{'form':form}))

        payload = {
                'content_html': content_html,
                'success': True,
            }
        return HttpResponse(json.dumps(payload), content_type="application/json")


def change_phone_number(request):
    if request.method == "POST":
        form = ModfiyPForm(request.POST)

        if form.is_valid():
            cd = form.clean()
            username = cd['username']
            _code = request.session.get('sms_code')
            smscode = cd['smscode']

            if  _code == int(smscode) :
                user = auth.get_user(request)
                user.username = username
                user.save()
                t = get_template('success.html')
                content_html = t.render(
                        RequestContext(request,{'form':form,'status':u'手机号修改成功！'}))

                payload = {
                        'content_html': content_html,
                        'success': True,
                    }
                return HttpResponse(json.dumps(payload), content_type="application/json")
            else:
                t = get_template('success.html')
                content_html = t.render(
                        RequestContext(request,{'form':form,'status':u'验证码错误！'}))

                payload = {
                        'content_html': content_html,
                        'success': True,
                    }
                return HttpResponse(json.dumps(payload), content_type="application/json")

        else:
            t = get_template('success.html')
            content_html = t.render(
                    RequestContext(request,{'form':form,'status':u'非法输入！'}))

            payload = {
                    'content_html': content_html,
                    'success': True,
                }
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        form = ModfiyPForm()
        t = get_template('changephone.html')
        content_html = t.render(
                RequestContext(request,{'form':form}))

        payload = {
                'content_html': content_html,
                'success': True,
            }
        return HttpResponse(json.dumps(payload), content_type="application/json")

def about_us(request):
    p = About_us.objects.filter(name=u"上海辞达金融信息服务有限公司")
    mediareports = MediaReports.objects.filter(status=1)

    return render_to_response('about.html',{'mediareports':mediareports,"description":p[0].description}, context_instance=RequestContext(request))

def guide(request):
    p = About_us.objects.all()
    p1 = RegistrationAgreement.objects.filter(name="mianzetiaokuan")
    return render_to_response('guide.html',{"p1":p1[0].agreement,"description":p[0].about_zhongtou}, context_instance=RequestContext(request))

def do_reminder(request):
    user = auth.get_user(request)
    return HttpResponse("ok")

#@login_required
def publish(request):
    user = auth.get_user(request)
    if request.method == "POST":
        form = PublishForm(request.POST)
        f = request.FILES.get('logo', None)
        if f:
            extension = os.path.splitext(f.name)[-1]
            msg = None
            if f.size > 1048576:
                msg = u"图片大小不能超过2MB"
            if (extension not in ['.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF']) or ('image' not in f.content_type):
                msg = u"图片格式必须为jpg，png，gif"
            if msg:
                return render_to_response("publish.html", {'form': form, 'error': msg},
                                          context_instance=RequestContext(request))   #返回用户信息页面

            im = Image.open(f)
            im.thumbnail((120, 120))
            name = 'logo' + storage.get_available_name(str(user.id)) + '.png'
            im.save('%s/%s' % (storage.location, name), 'PNG')
            logo_url = storage.url(name)
            print(logo_url)
        else:
            msg = u"请上传logo"
            return render_to_response("publish.html", {'form': form, 'error': msg},
                                          context_instance=RequestContext(request))


        f = request.FILES.get('plan', None)
        if f:
            extension = os.path.splitext(f.name)[-1]

            msg = None
            if f.size > 10485760:
                msg = u"文件大小不能超过20MB"
            if (extension not in ['.ppt', '.pptx', '.pdf', '.PPT', '.PPTX', '.PDF']):
                msg = u"文件格式必须为ppt，pptx，pdf"
            if msg:
                return render_to_response("publish.html", {'form': form, 'error': msg},
                                          context_instance=RequestContext(request))
            plan_url = handle_uploaded_file(f)
            print plan_url
        else:
            msg = u"请上传商业计划书"
            return render_to_response("publish.html", {'form': form, 'error': msg},
                                          context_instance=RequestContext(request))


        if form.is_valid():
            cd = form.cleaned_data
            project = cd['project']
            introduction = cd['introduction']
            description = cd['description']
            category = cd['category']
            status = cd['status']
            founder = cd['founder']
            flag = 0
            if project is None:
                form.valiatetype(2)
                flag =1
            elif flag != 1 and introduction is None:
                form.valiatetype(3)
                flag =1
            elif flag != 1 and description is None:
                form.valiatetype(4)
                flag =1
            elif flag !=1 and founder is None:
                form.valiatetype(5)
                flag =1

            if flag == 1:
                return render_to_response('publish.html',{'form':form}, context_instance=RequestContext(request))
            else:
                p1 = Project(name=cd['project'],introduction=cd['introduction'],description = cd['description'],category = cd['category'],status = cd['status'],founder = cd['founder'],business_plan_url=plan_url,logo=logo_url)
                p1.save()
                return render_to_response('publish.html',{'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('publish.html',{'form':form}, context_instance=RequestContext(request))
    else:
        form = PublishForm()

    return render_to_response('publish.html',{'form':form}, context_instance=RequestContext(request))

def investor_detail(request):
    return render_to_response('investor_detail.html',{}, context_instance=RequestContext(request))
def invested(request):

    inv = request.POST.get('inv')

    id = request.POST.get('project')
    per = request.POST.get('per')

    if inv and id:
        try:
            i = invest_detail.objects.get(invest_user=request.user,invest_project=Project.objects.get(id=id))
            i.invest_num = int(i.invest_num) + int(inv)
        except:
            i = invest_detail(invest_user=request.user,invest_project=Project.objects.get(id=id),\
                          invest_num=inv,invest_type=1,invest_amount=per)
        i.save()
        #计算总共投资了多少份
        f = invest_detail.objects.filter(invest_project=Project.objects.get(id=id))
        m = 0
        for i in f:
            m += int(i.invest_num)
        u = Project.objects.get(id=id)
        u.finish = m
        u.save()

        p = Project.objects.get(id=id)
        print "xxxx"
        try:
            sendmail.delay(request.user.username,p.name,inv)
        except:
            pass
        print "dddd"
        return HttpResponse(json.dumps({'t': 1}), content_type="application/json")
    return HttpResponse(json.dumps({'t': 0}), content_type="application/json")
def search_investor(request):
    #web(1:不限，3：认证资深投资人，2：认证投资人，)
    #web(4：不限，5：金融在线，6：电子商务, 7: 医疗, 8: 互联网, 9: 社交，10：生活服务)
    #sql(1:注册用户,2：认证资深投资人，3：认证投资人，4: 创业者),字段：authentication_class
    #sql(5：金融在线，6：电子商务, 7: 医疗, 8: 互联网, 9: 社交，10：生活服务)，字段：cate
    # ('1', '金融在线'),('2', '电子商务'),('3', '医疗'),('4', '互联网'),('5', '社交'),('6', '生活服务'),
    search_word = request.GET.getlist('search_word[]')
    print search_word
    if search_word == [u'1', u'4']:
        results = UserInformation.objects.all().order_by("-invest_class")
    elif search_word == [u'1', u'5']:
        results = UserInformation.objects.filter(cate=1).order_by("-invest_class")
    elif search_word == [u'1', u'6']:
        results = UserInformation.objects.filter(cate=2).order_by("-invest_class")
    elif search_word == [u'1', u'7']:
        results = UserInformation.objects.filter(cate=3).order_by("-invest_class")
    elif search_word == [u'1', u'8']:
        results = UserInformation.objects.filter(cate=4).order_by("-invest_class")
    elif search_word == [u'1', u'9']:
        results = UserInformation.objects.filter(cate=5).order_by("-invest_class")
    elif search_word == [u'1', u'10']:
        results = UserInformation.objects.filter(cate=6).order_by("-invest_class")
    elif search_word == [u'1', u'11']:
        results = UserInformation.objects.filter(cate=7).order_by("-invest_class")
    elif search_word == [u'1', u'12']:
        results = UserInformation.objects.filter(cate=8).order_by("-invest_class")
    elif search_word == [u'1', u'13']:
        results = UserInformation.objects.filter(cate=9).order_by("-invest_class")
    elif search_word == [u'2', u'4']:
        results = UserInformation.objects.filter(invest_class=2).order_by("-invest_class")
    elif search_word == [u'2', u'5']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=1).order_by("-invest_class")
    elif search_word == [u'2', u'6']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=2).order_by("-invest_class")
    elif search_word == [u'2', u'7']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=3).order_by("-invest_class")
    elif search_word == [u'2', u'8']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=4).order_by("-invest_class")
    elif search_word == [u'2', u'9']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=5).order_by("-invest_class")
    elif search_word == [u'2', u'10']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=6).order_by("-invest_class")
    elif search_word == [u'2', u'11']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=7).order_by("-invest_class")
    elif search_word == [u'2', u'12']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=8).order_by("-invest_class")
    elif search_word == [u'2', u'13']:
        results = UserInformation.objects.filter(invest_class=2).filter(cate=9).order_by("-invest_class")

    elif search_word == [u'3', u'4']:
        results = UserInformation.objects.filter(invest_class=3).order_by("-invest_class")
    elif search_word == [u'3', u'5']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=1).order_by("-invest_class")
    elif search_word == [u'3', u'6']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=2).order_by("-invest_class")
    elif search_word == [u'3', u'7']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=3).order_by("-invest_class")
    elif search_word == [u'3', u'8']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=4).order_by("-invest_class")
    elif search_word == [u'3', u'9']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=5).order_by("-invest_class")
    elif search_word == [u'3', u'10']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=6).order_by("-invest_class")
    elif search_word == [u'3', u'11']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=7).order_by("-invest_class")
    elif search_word == [u'3', u'12']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=8).order_by("-invest_class")
    elif search_word == [u'3', u'13']:
        results = UserInformation.objects.filter(invest_class=3).filter(cate=9).order_by("-invest_class")
    else:
        results = UserInformation.objects.all().order_by("-invest_class")
    a = []
    s = []
    u = UserInformation.objects.get(user=request.user).attention_persion.all()
    for i in results:
        b=0.0
        r = invest_detail.objects.filter(invest_user=i.user)
        #r=i.user.invest_user_set
        if r:
            for j in r:
                b+=float(j.invest_amount)*float(j.invest_num)
        a.append(b)

        if i.user in u:
            s.append(1)
        else:
            s.append(0)

    ppp = Paginator(results, 10)
    ppp1 = Paginator(a,10)
    ppp2 = Paginator(s,10)
    try:
            page = int(request.GET.get('page', '1'))
    except ValueError:
            page = 1
    try:
            results = ppp.page(page)
            a= ppp1.page(page)
            s = ppp2.page(page)
    except (EmptyPage, InvalidPage):
            results = ppp.page(ppp.num_pages)
            a= ppp1.page(ppp.num_pages)
            s = ppp2.page(ppp.num_pages)
    last_page = ppp.page_range[len(ppp.page_range) - 1]
    page_set = get_pageset(last_page, page)
    t = get_template('search_result_investor.html')

    c = {'results': results, "s":s, "amount":a,'last_page': last_page, 'page_set': page_set} #make a name
    content_html = t.render(
            RequestContext(request,c ))
    payload = {
            'content_html': content_html,
            'success': True
        }
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required
def investor(request):
    return render_to_response('investor.html',{}, context_instance=RequestContext(request))

def prodetails(request,objectid):
    p = Project.objects.get(id=objectid)
    forum = project_forum.objects.filter(forum_project=p)
    invest_de = invest_detail.objects.filter(invest_project=p)
    amount = 0
    try:
        attention_pr =   Project.objects.filter(click=request.user)
        if p in attention_pr:
            flag = 1
        else:
            flag = 0
    except:
        flag = 0
    for i in invest_de:
        amount += int(i.invest_num)
    return render_to_response('prodetails.html',{"flag":flag,"result":p,"project_forum":forum,'amount':amount,'invest_detail':invest_de}, context_instance=RequestContext(request))


def project(request,objectid):

    return render_to_response('project.html',{"objectid":[int(objectid),14]}, context_instance=RequestContext(request))

def invest_pr(request,objectid):
    p = Project.objects.get(id=objectid[:-1])

    return render_to_response('invest_pr.html',{"invest_type":int(objectid[-1]),"project":p}, context_instance=RequestContext(request))



def add_attion(request,objectid):
    t = Project.objects.get(id=objectid)
    count = len(t.click.all()) + 1

    t.click.add(request.user)
    t.save()
    t = Project.objects.get(id=objectid)
    count1 = len(t.click.all())
    if count != count1:
        comment = u"你已经关注了该项目！"
    else:
        comment = u"关注成功！"
    return HttpResponse(json.dumps({'attion': count1,"comment":comment}), content_type="application/json")

def cancel_attion(request,objectid):

    t = Project.objects.get(id=objectid)
    t.click.remove(request.user)
    t.save()

    return HttpResponse(json.dumps({"comment":1}), content_type="application/json")

def add_attion_investor(request):
    t =User.objects.get(username=request.POST.get("investor"))
    u = UserInformation.objects.get(user=request.user)
    if t not in u.attention_persion.all():
        u.attention_persion.add(t)
        u.save()
    return HttpResponse(json.dumps({'attion': 56,"comment":1}), content_type="application/json")

def cancel_attion_investor(request):
    t = User.objects.get(username=request.POST.get("investor"))
    u = UserInformation.objects.get(user=request.user)
    u.attention_persion.remove(t)
    u.save()
    return HttpResponse(json.dumps({}), content_type="application/json")

def get_status(request):
    t = User.objects.get(id=request.POST.get("investor"))
    u = UserInformation.objects.get(user=request.user)
    if t in u.attention_persion.all():
        flag = 1
    else:
        flag = 0
    return HttpResponse(json.dumps({"flag":flag}), content_type="application/json")

def sendSMS(request):
    u = User.objects.get(username=request.POST.get("investor"))
    content = request.POST.get("content")
    if content:
        t = Signal.objects.create(type=2,user=request.user,who=u,content=content)
        t.save()
        return HttpResponse(json.dumps({"success":1}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success":0}), content_type="application/json")

def delete_signal(request):
    signal = Signal.objects.get(id=request.POST.get('id'))
    signal.delete()
    return HttpResponse(json.dumps({"success":0}), content_type="application/json")

def search_project(request):
    #web(1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例)
    #web(14：不限，15：金融在线，16：电子商务, 17: 医疗, 18: 互联网, 19: 社交，20：生活服务)
    #sql(14：不限，15：金融在线，16：电子商务, 17: 医疗, 18: 互联网, 19: 社交，20：生活服务)
    search_word = request.GET.getlist('search_word[]')
    if search_word is not None:
        if int(search_word[1]) == 14 and int(search_word[0]) != 1 :
            if int(search_word[0]) == 2 :
                results = Project.objects.filter(active=1)
            elif int(search_word[0]) == 3 :
                results = Project.objects.filter(status=0)
            elif int(search_word[0]) == 4 :
                results = Project.objects.filter(status=1)
            elif int(search_word[0]) == 5 :
                results = Project.objects.filter(status=2)
            elif int(search_word[0]) == 6 :
                results = Project.objects.filter(status=2)

        elif int(search_word[0]) == 1 and int(search_word[1]) != 14:
            results = Project.objects.filter(category=int(search_word[1])-14)
        elif int(search_word[0]) != 1 and int(search_word[1]) != 14 :
            if int(search_word[0]) == 2 :
                results = Project.objects.filter(active=1).filter(category=int(search_word[1])-14)
            else:
                results = Project.objects.filter(status=int(search_word[0])-3).filter(category=int(search_word[1])-14)
        else:
            results = Project.objects.all()
    else :
        results = Project.objects.all()

    ppp = Paginator(results, 20)
    try:
            page = int(request.GET.get('page', '1'))
    except ValueError:
            page = 1
    try:
            results = ppp.page(page)
    except (EmptyPage, InvalidPage):
            results = ppp.page(ppp.num_pages)
    last_page = ppp.page_range[len(ppp.page_range) - 1]
    page_set = get_pageset(last_page, page)
    t = get_template('search_result_single.html')
    content_html = t.render(
            RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
    payload = {
            'content_html': content_html,
            'success': True
        }
    return HttpResponse(json.dumps(payload), content_type="application/json")

def search(request):
    #web(1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例)
    #web(14：不限，15：金融在线，16：电子商务, 17: 医疗, 18: 互联网, 19: 社交，20：生活服务)
    search_word = request.GET.get('search_word[]',None)
    if search_word is not None:
        if int(search_word) == 2 :
            results = Project.objects.filter(active=1)
        elif int(search_word) == 3 :
            results = Project.objects.filter(status=0)
        elif int(search_word) == 4 :
            results = Project.objects.filter(status=1)
        elif int(search_word) == 5 :
            results = Project.objects.filter(status=2)
        elif int(search_word) == 6 :
            results = Project.objects.filter(status=2)
        else :
            results = Project.objects.all()
    else :
        results = Project.objects.all()

    ppp = Paginator(results, 20)
    try:
            page = int(request.GET.get('page', '1'))
    except ValueError:
            page = 1
    try:
            results = ppp.page(page)
    except (EmptyPage, InvalidPage):
            results = ppp.page(ppp.num_pages)
    last_page = ppp.page_range[len(ppp.page_range) - 1]
    page_set = get_pageset(last_page, page)
    t = get_template('search_result_single.html')
    content_html = t.render(
            RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
    payload = {
            'content_html': content_html,
            'success': True
        }
    return HttpResponse(json.dumps(payload), content_type="application/json")
def project_reply(request,project_id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(u'只有登录用户才能评论!')
        _code = request.POST.get('log_code')
        if not _code:
            return HttpResponse(u'请输入验证码!')
        else:
            ca = Captcha(request)
            if ca.check(_code):

                t = project_forum()
                if request.POST['content']:
                    t.forum_content = request.POST['content']
                else:
                    return HttpResponse(u'输入内容不能为空!')
                print "rrrr"
                t.forum_content = t.forum_content.replace("<img>", "<img class = 'bbs_topic_img' src='")
                t.forum_content = t.forum_content.replace("</img>", "'/>")
                t.forum_content = t.forum_content.replace("\r\n", "<br/>")
                print "555"
                print project_id,Project.objects.filter(id=project_id)[0]
                t.forum_project = Project.objects.filter(id=project_id)[0]
                print "yyy"
                print request.user
                t.forum_user = request.user
                t.save()
                return HttpResponse(1)
            else:
                return HttpResponse(u'请输入验证码有误!')


def search_zc(request):
    #1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例
    search_word = request.GET.get('search_word',None)
    results = None
    if search_word is not None:
        if int(search_word) == 2 :
            results = Project.objects.filter(active=1).distinct()
        elif int(search_word) == 3 :
            results_hot = Project.objects.filter(status=0).distinct()
        elif int(search_word) == 4 :
            results = Project.objects.filter(status=1).distinct()
        elif int(search_word) == 5 :
            results = Project.objects.filter(status=2).distinct()
        elif int(search_word) == 6 :
            results = Project.objects.filter(status=2).distinct()
        else :
            results = Project.objects.all().distinct()
    else :
        results = Project.objects.all().distinct()
    if results :
        ppp = Paginator(results, 4)
    else:
        ppp = Paginator(results_hot, 8)
    try:
            page = int(request.GET.get('page', '1'))
    except ValueError:
            page = 1
    try:
            results = ppp.page(page)
    except (EmptyPage, InvalidPage):
            results = ppp.page(ppp.num_pages)
    last_page = ppp.page_range[len(ppp.page_range) - 1]
    page_set = get_pageset(last_page, page)
    t = get_template('search_result_zc.html')
    content_html = t.render(
            RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
    payload = {
            'content_html': content_html,
            'success': True
        }
    return HttpResponse(json.dumps(payload), content_type="application/json")

def investor_info(request,objectid):
    p1 = UserInformation.objects.get(user=User.objects.get(username=objectid))

    return render_to_response('investor_intro.html',{"investor_info":p1}, context_instance=RequestContext(request))

def safety(request, objectid):
    if int(objectid) == 1:
        name = u"项目风控"
        ag = RegistrationAgreement.objects.filter(name="wind_control")
    elif int(objectid) == 2:
        name = u"资金保障"
        ag = RegistrationAgreement.objects.filter(name="fund_security")
    elif int(objectid) == 3:
        name = u"财务监管系统"
        ag = RegistrationAgreement.objects.filter(name="financial_supervision")
    elif int(objectid) == 4:
        name = u"技术保障"
        ag = RegistrationAgreement.objects.filter(name="technical_support")
    return render_to_response('safety.html',{"name":name, "agreement":ag[0].agreement}, context_instance=RequestContext(request))

def intermediary(request, objectid):
    if int(objectid) == 1:
        file_name = '/root/zc/static/download/有限合伙协议.htm'
    elif int(objectid) == 2:
        file_name = '/root/zc/static/download/股权转让协议.htm'
    elif int(objectid) == 3:
        file_name = '/root/zc/static/download/融资居间协议.htm'
    elif int(objectid) == 4:
        file_name = '/root/zc/static/download/投资协议.htm'
    elif int(objectid) == 5:
        file_name = '/root/zc/static/download/认购意向书协议.htm'
    elif int(objectid) == 6:
        file_name = '/root/zc/static/download/注册协议.htm'
    elif int(objectid) == 7:
        file_name = '/root/zc/static/download/服务协议.htm'

    response = HttpResponse(readFile(file_name))
    return response


def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()

def handle_uploaded_file(f):
    path = '/root/zc/static/project/'
    file_name = path + f.name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return file_name

def get_pageset(last_page, pagenum):
    page_set = []
    if pagenum <= 3:
        start = 0
        end = 6
    elif pagenum > last_page - 3:
        start = last_page - 4
        end = last_page + 1
    else:
        start = pagenum - 2
        end = pagenum + 3
    for i in range(start, end, 1):
        if i <= 0:
            pass
        elif i > last_page:
            break
        else:
            page_set.append(i)
    return page_set


def uploadify_script(request,objectid):
    ret="0"
    file = request.FILES.get("Filedata",None)
    if file:
        result,new_name=profile_upload(file,request,objectid)
        if result:
            ret="1"
        else:
            ret="2"
    json={'ret':ret,'save_name':new_name}
    return HttpResponse(simplejson.dumps(json,ensure_ascii = False))

def profile_upload(file,request,objectid):
    '''文件上传函数'''
    if file:
        u = UserInformation.objects.get(user=request.user)
        im = Image.open(file)
        im.thumbnail((120, 120))
        if int(objectid)== 0:
            name = 'icard' + storage.get_available_name(str(request.user.id)) +file.name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            u.id_card = url
        elif int(objectid)== 1:
            name = 'financial_assets' + storage.get_available_name(str(request.user.id)) +file.name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            u.financial_assets = url
        elif int(objectid)== 2:
            name = 'fixed_assets' + storage.get_available_name(str(request.user.id)) +file.name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            u.fixed_assets = url
        elif int(objectid)== 3:
            name = 'income_assets' + storage.get_available_name(str(request.user.id)) +file.name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            u.income_assets = url
        u.save()
        return (True,name) #change

def profile_delte(request):
    del_file=request.POST.get("delete_file",'')
    if del_file:
        path_file=os.path.join(settings.MEDIA_ROOT,'upload',del_file)
        os.remove(path_file)

def do_search(request):
    print request
    if request.method == 'POST':
        keyword = request.POST.get('keyword',u'0')
        if keyword and keyword != u'0':
            try:
                results = Project.objects.filter(Q(publish__username__icontains=keyword)\
                        |Q(name__icontains=keyword)|Q(category__icontains=keyword))
            except Exception as e:
                results = Project.objects.all()
        else:
            results = Project.objects.all()

        ppp = Paginator(results, 20)

        try:
                page = int(request.POST.get('page', '1'))
        except ValueError:
                page = 1
        try:
                results = ppp.page(page)
        except (EmptyPage, InvalidPage):
                results = ppp.page(ppp.num_pages)
        last_page = ppp.page_range[len(ppp.page_range) - 1]
        page_set = get_pageset(last_page, page)

        t = get_template('do_search_project.html')
        content_html = t.render(
                RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
        payload = {
                'content_html': content_html,
                'success': True
            }
        return HttpResponse(json.dumps(payload), content_type="application/json")

    else:
        return HttpResponseRedirect(reverse('do_result'))
def do_result(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword','')
        if not keyword:
            keyword = 0
        page = request.POST.get('page', '1')

        return render_to_response('investor_search.html',{'keyword':keyword,'page':page},context_instance=RequestContext(request))

