# coding=utf-8

import MySQLdb
import datetime
from itertools import chain
import json
import os
import random

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

from searcher.forms import ContactForm, SearchForm, LoginForm, UserInformationForm, RegisterForm, ForgetPWForm, ModfiyPWForm, PublishForm
from searcher.inner_views import index_loading, data_filter, result_sort, get_pageset, get_user_filter, user_auth, \
    refresh_header,send_flow_all,user_get_ip
from searcher.models import Bid, UserFavorite, Platform, UserInformation, DimensionChoice, UserFilter, UserReminder, \
    WeekHotSpot, BidHis, ReminderUnit, About_us, Partners, Frendlink, Project,project_forum,Signal
from ddbid import conf
from django.db.models import Q


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
                        return HttpResponseRedirect(reverse('index_zc'))
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
    print "this views forgetpw"
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
    print "checkuser"
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

def register(request):
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
                return  render_to_response("reg_success.html", {'flag1':flag1}, context_instance=RequestContext(request))
        else:
            return render_to_response("signup.html", {'form': form}, context_instance=RequestContext(request))
    else:
        form = RegisterForm()
        return render_to_response("signup.html", {'form': form}, context_instance=RequestContext(request))


@login_required
def logout(request):
    """

    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('index_jf'))


@login_required
def add_favoritebid(request, objectid):
    user_id = auth.get_user(request).id
    user = User.objects.get(id=user_id)
    ftype = 1
    u = UserFavorite.objects.filter(user_id=user_id, favorite_type=ftype, favorite_id=objectid)
    if u.exists():
        return HttpResponse(u'已经收藏过了')

    u1 = UserFavorite(user_id=user_id, favorite_type=ftype, favorite_id=objectid)
    u1.save()
    return HttpResponse(u'收藏成功')


@login_required
def add_favoriteplatform(request, objectid):
    user_id = auth.get_user(request).id
    user = User.objects.get(id=user_id)
    ftype = 2
    u = UserFavorite.objects.filter(user_id=user_id, favorite_type=ftype, favorite_id=objectid)
    if u.exists():
        return HttpResponse(u'已经收藏过了')
    u1 = UserFavorite(user_id=user_id, favorite_type=ftype, favorite_id=objectid)
    u1.save()
    return HttpResponse(u'收藏成功')


@login_required
def add_reminder(request, objectid):
    user = auth.get_user(request)
    try:
        u_r = UserReminder.objects.get(user=user, bid=objectid)
        return HttpResponse(u'已存在')
    except ObjectDoesNotExist:
        u_r = UserReminder(user=user, bid=objectid, reminder=1, value=1, status=1)
        u_r.save()
        return HttpResponse(u'已添加')

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


def platform(request):
    pfs = Platform.objects.all()
    # print(pfs)
    return render_to_response("platform.html", {'platforms': pfs}, context_instance=RequestContext(request))


@login_required
def userinfo(request):
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
            name = 'photo_user' + storage.get_available_name(str(user.id)) + '.png'
            print name
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
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
        leader  = Project.objects.filter(leader=user)
        #跟投项目
        invest = Project.objects.filter(investor=user)
        #我发布的项目
        publish_pr = Project.objects.filter(publish=user)
        #我关注的项目
        attention_pr = user.userinformation.industry
        if request.user.is_authenticated():
            signal =  Signal.objects.filter(who=request.user)
            print signal
        else:
            signal = []

    return render_to_response("userinfo.html", {"signal":signal,'form': form,"leader":leader,"invest":invest,"publish_pr":publish_pr,"attention_pr":attention_pr},
                              context_instance=RequestContext(request))

@login_required
def userinformation(request):
    url = None
    user = auth.get_user(request)
    flag = 1
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        f = request.FILES.get('file', None)
        if f:
            extension = os.path.splitext(f.name)[-1]
            msg = None
            if f.size > 1048576:
                msg = u"图片大小不能超过1MB"
            if (extension not in ['.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF']) or ('image' not in f.content_type):
                msg = u"图片格式必须为jpg，png，gif"
            if msg:
                return render_to_response("user_information.html", {'form': form, 'flag': flag, 'error': msg},
                                          context_instance=RequestContext(request))

            im = Image.open(f)
            im.thumbnail((120, 120))
            name = 'photo' + storage.get_available_name(str(user.id)) + '.png'
            im.save('%s/%s' % (storage.location, name), 'PNG')
            url = storage.url(name)
            # print(url)

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
            return render_to_response("user_information.html", {'form': form, 'flag': flag},
                                      context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('userinformation'))
    else:
        try:
            form = UserInformationForm(instance=user.userinformation)
        except ObjectDoesNotExist:
            form = UserInformationForm()
            # print(form)
    return render_to_response("user_information.html", {'form': form, 'flag': flag},
                              context_instance=RequestContext(request))

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
               """ % ("shcdjr", m.hexdigest().upper(), int(phoneNum), content.decode("utf-8").encode("GBK"))

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
                   """ % ("shcdjr", m.hexdigest().upper(), int(phoneNum), content.decode("utf-8").encode("GBK"))

            cookies = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookies)
            request = urllib2.Request(
                                       url = r'http://userinterface.vcomcn.com/Opration.aspx',
                                       headers= {'Content-Type':'text/xml'},
                                       data = data
                                      )
        return HttpResponse()




def index(request):
    return render_to_response('index.html',{}, context_instance=RequestContext(request))


def agreement(request):

    ag = RegistrationAgreement.objects.filter(name="registration_agreement")
    print "ag is :",ag
    return render_to_response('agreement.html',{'agreement':ag[2].agreement}, context_instance=RequestContext(request))


def index_zc(request):
    #1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例

    daily_selection = Project.objects.filter(active=1).distinct()[0:4]

    preheating = Project.objects.filter(status=0).distinct()[0:8]

    crowdfunded = Project.objects.filter(status=1).distinct()[0:4]

    crowdfunded_success = Project.objects.filter(status=2).distinct()[0:4]

    crowdfunded_finsh= Project.objects.filter(status=2).distinct()[0:4]

    return render_to_response('index_page.html',{"daily_selection":daily_selection,"preheating":preheating, \
                              "crowdfunded":crowdfunded,"crowdfunded_success":crowdfunded_success,\
                                         "crowdfunded_finsh":crowdfunded_finsh},context_instance=RequestContext(request))

def index_jf(request):

    return render_to_response('home.html',{}, context_instance=RequestContext(request))

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
            print "form error",form.errors
            print "form is not valid kkkkkk"

            print "xxxxxxxxxxxxxxxx"
            t = get_template('success.html')
            content_html = t.render(
                    RequestContext(request,{'form':form,'status':u'输入非法！'}))

            payload = {
                    'content_html': content_html,
                    'success': True,
                }
            return HttpResponse(json.dumps(payload), content_type="application/json")

    else:
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
        form = ForgetPWForm(request.POST)
        if form.is_valid():
            cd = form.clean()
            username = cd['username']
            _code = dict_code.get('smscode')
            smscode = cd['smscode']

            print _code ,smscode

            if  _code == int(smscode) :
                print "11111"
                user = auth.get_user(request)
                user.username = username
                user.save()
                form.valiatetype(10)
                return render_to_response('userinfo.html',{"form":form},
                                      context_instance=RequestContext(request))
            else:
                form.valiatetype(2)
                return render_to_response('userinfo.html',{"form":form},
                                      context_instance=RequestContext(request))

        else:
            return render_to_response('userinfo.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = ForgetPWForm()
        t = get_template('changephone.html')
        content_html = t.render(
                RequestContext(request,{'form':form}))

        payload = {
                'content_html': content_html,
                'success': True,
            }
        return HttpResponse(json.dumps(payload), content_type="application/json")



def about_us(request):
    p1 = RegistrationAgreement.objects.filter(name="mianzetiaokuan")
    p2 = About_us.objects.filter(name=u"上海辞达金融信息服务有限公司")
    return render_to_response('about.html',{"p1":p1[0].agreement,"description":p2[0].description}, context_instance=RequestContext(request))

def guide(request):
    p = About_us.objects.all()

    return render_to_response('guide.html',{"description":p[0].about_zhongtou}, context_instance=RequestContext(request))

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
            print extension
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

def search_investor(request):
    #web(1:不限，2：认证资深投资人，3：认证投资人，)
    #web(4：不限，5：金融在线，6：电子商务, 7: 医疗, 8: 互联网, 9: 社交，10：生活服务)
    #sql(1:注册用户,2：认证资深投资人，3：认证投资人，4: 创业者),字段：authentication_class
    #sql(5：金融在线，6：电子商务, 7: 医疗, 8: 互联网, 9: 社交，10：生活服务)，字段：cate
    # ('1', '金融在线'),('2', '电子商务'),('3', '医疗'),('4', '互联网'),('5', '社交'),('6', '生活服务'),
    search_word = request.GET.getlist('search_word[]')
    print search_word
    if search_word == [u'1', u'4']:
        results = UserInformation.objects.all()
    elif search_word == [u'1', u'5']:
        results = UserInformation.objects.filter(industry='1')
        for i in results:
            print i.cate
        print results
    elif search_word == [u'1', u'6']:
        results = UserInformation.objects.filter(industry='2')
    elif search_word == [u'1', u'7']:
        results = UserInformation.objects.filter(industry=3)
    elif search_word == [u'1', u'8']:
        results = UserInformation.objects.filter(industry=4)
    elif search_word == [u'1', u'9']:
        results = UserInformation.objects.filter(industry=5)
    elif search_word == [u'1', u'10']:
        results = UserInformation.objects.filter(industry=6)
    elif search_word == [u'2', u'4']:
        results = UserInformation.objects.filter(authentication_class=2)
    elif search_word == [u'2', u'5']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=1)
    elif search_word == [u'2', u'6']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=2)
    elif search_word == [u'2', u'7']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=3)
    elif search_word == [u'2', u'8']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=4)
    elif search_word == [u'2', u'9']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=5)
    elif search_word == [u'2', u'10']:
        results = UserInformation.objects.filter(authentication_class=2).filter(industry=6)
    elif search_word == [u'3', u'4']:
        results = UserInformation.objects.filter(authentication_class=3)
    elif search_word == [u'3', u'5']:
        results = UserInformation.objects.filter(authentication_class=3).filter(industry=1)
    elif search_word == [u'3', u'6']:
        results = UserInformation.objects.filter(authentication_class=3).filter(industry=2)
    elif search_word == [u'3', u'7']:
        results = UserInformation.objects.filter(authentication_class=3).filter(industry=3)
    elif search_word == [u'3', u'8']:
        results = UserInformation.objects.filter(authentication_class=3).filter(industry=4)
    elif search_word == [u'3', u'9']:
        results = UserInformation.objects.filter(authentication_class=3).filter(industry=5)
    elif search_word == [u'3', u'10']:
       results = UserInformation.objects.filter(authentication_class=3).filter(industry=6)
    else:
        results = UserInformation.objects.all()

    print "ppppp"
    ppp = Paginator(results, 10)

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
    t = get_template('search_result_investor.html')
    content_html = t.render(
            RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
    payload = {
            'content_html': content_html,
            'success': True
        }
    return HttpResponse(json.dumps(payload), content_type="application/json")

def investor(request):
    return render_to_response('investor.html',{}, context_instance=RequestContext(request))

def prodetails(request,objectid):
    p = Project.objects.get(id=objectid)
    forum = project_forum.objects.filter(forum_project=p)
    return render_to_response('prodetails.html',{"result":p,"project_forum":forum}, context_instance=RequestContext(request))


def project(request,objectid):

    return render_to_response('project.html',{"objectid":[int(objectid),14]}, context_instance=RequestContext(request))

def invest_pr(request,objectid):
    p = Project.objects.get(id=objectid[:-1])
    print objectid[-1],type(objectid[-1])
    return render_to_response('invest_pr.html',{"invest_type":int(objectid[-1]),"project":p}, context_instance=RequestContext(request))

def add_attion(request,objectid):
    t = Project.objects.get(id=objectid)
    count = len(t.click.all()) + 1

    t.click.add(request.user)
    t.save()
    t = Project.objects.get(id=objectid)
    count1 = len(t.click.all())
    if count != count1:
        comment = u"你已经关注了改用户！"
    else:
        comment = u"关注成功！"
    return HttpResponse(json.dumps({'attion': count1,"comment":comment}), content_type="application/json")

def add_attion_investor(request):
    t = UserInformation.objects.get(id=request.POST.get("investor"))

    attention_persion = len(t.attention_persion.all()) + 1

    t.attention_persion.add(request.user)
    t.save()
    t = UserInformation.objects.get(id=request.POST.get("investor"))
    attention_persion_after = len(t.attention_persion.all())
    if attention_persion != attention_persion_after:
        comment = u"你已经关注了该用户！"
    else:
        comment = u"关注成功！"

    return HttpResponse(json.dumps({'attion': attention_persion_after,"comment":comment}), content_type="application/json")

def sendSMS(request):
    u = User.objects.get(id=request.POST.get("investor"))
    content = request.POST.get("content")

    if content:
        t = Signal.objects.create(type=2,user=request.user,who=u,content=content)
        t.save()
        return HttpResponse(json.dumps({"success":1}), content_type="application/json")
    else:
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
            if int(search_word[1]) == 15 :
                results = Project.objects.filter(category=1)
            elif int(search_word[1]) == 16 :
                results = Project.objects.filter(category=2)
            elif int(search_word[1]) == 17 :
                results = Project.objects.filter(category=3)
            elif int(search_word[1]) == 18 :
                results = Project.objects.filter(category=4)
            elif int(search_word[1]) == 19 :
                results = Project.objects.filter(category=5)
            elif int(search_word[1]) == 20 :
                results = Project.objects.filter(category=6)
        elif int(search_word[0]) != 1 and int(search_word[1]) != 14 :
            if int(search_word[0]) == 2 :
                results = Project.objects.filter(active=1).filter(category=int(search_word[1])-14)
            else:
                results = Project.objects.filter(status=int(search_word[0])).filter(category=int(search_word[1])-14)
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
                print "dddd"
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
def do_reminder(request):
    user = auth.get_user(request)
    return HttpResponse("ok")

def do_result(request):
    if request.method == 'POST':
        select = request.POST.get('select','')
        keyword = request.POST.get('keyword','')
        if not keyword:
            keyword = 0
        page = request.POST.get('page', '1')

        return render_to_response('investor_search.html',{'select':select,'keyword':keyword,'page':page},context_instance=RequestContext(request))
def do_search(request):
    print request,request.method
    if request.method == 'POST':
        select = request.POST.get('select','')
        keyword = request.POST.get('keyword','')

        print select,type(select)
        if select == u"找项目":
            if keyword and keyword != u'0':
                try:
                    results = Project.objects.filter(Q(publish__username__icontains=keyword)\
                            |Q(name__icontains=keyword)|Q(category__icontains=keyword))
                except Exception as e:
                    results = Project.objects.all()
                print results
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
            print last_page,page
            t = get_template('do_search_project.html')
            content_html = t.render(
                    RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
            payload = {
                    'content_html': content_html,
                    'success': True
                }
            return HttpResponse(json.dumps(payload), content_type="application/json")
        else:
            print keyword,type(keyword)
            if keyword and keyword != u'0':
                results = User.objects.filter(Q(username__icontains=keyword)|Q(userinformation__realname__icontains=keyword))
            else:
                results = User.objects.all()
            ppp = Paginator(results, 10)

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
            t = get_template('do_search_investor.html')
            content_html = t.render(
                    RequestContext(request, {'results': results, 'last_page': last_page, 'page_set': page_set}))
            payload = {
                    'content_html': content_html,
                    'success': True
                }
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        return HttpResponseRedirect(reverse('do_result'))


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
    print p1.realname, p1.position, p1.industry, p1.authentication_class
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
    print objectid,type(objectid)
    if int(objectid) == 1:
        file_name = '/root/zc/static/download/融资居间协议.htm'
    elif int(objectid) == 2:
        file_name = '/root/zc/static/download/有限合伙协议.htm'
    elif int(objectid) == 3:
        file_name = '/root/zc/static/download/投资协议.htm'
    elif int(objectid) == 4:
        file_name = '/root/zc/static/download/股权转让协议.htm'

    response = HttpResponse(readFile(file_name))
    return response


def readFile(fn, buf_size=262144):
    print fn
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