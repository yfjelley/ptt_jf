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

from searcher.forms import ContactForm, SearchForm, LoginForm, UserInformationForm, RegisterForm, ForgetPW, ModfiyPW, PublishForm
from searcher.inner_views import index_loading, data_filter, result_sort, get_pageset, get_user_filter, user_auth, \
    refresh_header
from searcher.models import Bid, UserFavorite, Platform, UserInformation, DimensionChoice, UserFilter, UserReminder, \
    WeekHotSpot, BidHis, ReminderUnit, About_us, Partners, Frendlink, Project
from ddbid import conf


from searcher.models import RegistrationAgreement


__author__ = 'pony'

storage = FileSystemStorage(
    location=conf.UPLOAD_PATH,
    base_url='/static/upload/'
)

dict_code = {}

def login(request):
    if request.method == 'POST':
        print "this is post"
        username = request.REQUEST.get('log_un', None)
        pwd = request.REQUEST.get('log_pwd', None)
        if username is None:
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.clean()
                username = cd['username']
                pwd = cd['password']
                user = auth.authenticate(username=username, password=pwd)
                print "user is %s" % user
                if user is None:
                    form.valiatetype(4)
                    print form
                    return render_to_response("login.html", {'form': form}, context_instance=RequestContext(request))
                else:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('index_jf'))

            else:
                return render_to_response('login.html', {'form': form, },
                                          context_instance=RequestContext(request))
    else:
        form = LoginForm()
        print "this is get"
        return render_to_response('login.html', {'form': form},
                                  context_instance=RequestContext(request))

def forgetpw(request):
    if request.method == 'POST':
        form = ForgetPW(request.POST)
        if form.is_valid():
            cd = form.clean()
            username = cd['username']
            _code = dict_code.get('smscode')
            smscode = cd['smscode']
            user = User.objects.get(username=username)
            pw = user.userinformation.abcdefg
            print type(pw), type(smscode), type(_code)

            if pw is not None and _code == int(smscode):
                user = auth.authenticate(username=username, password=pw)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index_jf'))

            else:
                form.valiatetype(2)
                return render_to_response('forgetpwd.html',{"form":form},
                                      context_instance=RequestContext(request))


        else:
            return render_to_response('forgetpwd.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = ForgetPW()
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
        if _code.lower() == vcode.lower():
            response.write('{"info": "","status": "y"}')
            return response
        else:
            response.write('{"info": "验证码错误","status": "n"}')
            return response

def checksmscode(request):
    if_smscode = request.POST.get('name', None)
    print dict_code
    _code = dict_code['smscode']
    print _code
    if if_smscode:
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        smscode = request.POST.get('param', None)
        print "smscode type %s %s"%(type(smscode), smscode)
        print "_code type %s %s"%(type(_code), _code)
        if _code  == int(smscode):
            response.write('{"info": "","status": "y"}')
            return response
        else:
            response.write('{"info": "验证码错误","status": "n"}')
            return response

def register(request):
    if request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"

        u_ajax = request.POST.get('name', None)
        if u_ajax:
            response['Content-Type'] = "application/json"
            u = User.objects.filter(username=u_ajax)
            if u.exists():
                return HttpResponse(u'用户已存在')

        form = RegisterForm(request.POST)


        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            print "xxxxxxxxxxxxxxxxx"
            pwd1 = cd['password']
            pwd2 = cd['password2']

            code = cd['vcode']
            smscode = cd['smscode']
            ca = Captcha(request)
            flag = 0
            u = User.objects.filter(username=username)
            print "u %s"% u
            f = ca.check(code)
            if u.exists():
                form.valiatetype(2)
                print "flag2"
                flag = 1
            elif flag != 1 and pwd1 != pwd2:
                form.valiatetype(3)
                print "flag3"
                flag = 1
            elif flag != 1 and not f:
                form.valiatetype(4)
                print "flag4"
                flag = 1

            elif flag != 1 and dict_code.get('smscode') != int(smscode):
                form.valiatetype(5)
                flag = 1

            if flag == 1:
                print "yyyyyyyyyyyyyyyyy"
                return render_to_response("signup.html", {'form': form}, context_instance=RequestContext(request))
            elif pwd1 == pwd2 and f:
                new_user = User.objects.create_user(username=username, password=pwd1)
                new_user.save()

                u = UserInformation(user=new_user, photo_url='/static/upload/default.png', abcdefg=pwd1)
                u.save()
                user = auth.authenticate(username=username, password=pwd1)
                auth.login(request, user)

                return HttpResponseRedirect(reverse('index_jf'))
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
    form = UserInformationForm()
    formPW = ModfiyPW()
    """
    if request.method == 'POST':
        form  = UserInformationForm(request.POST)
        f = request.FILES.get('file',None)
        if f:
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
            # print(form)
    """
    return render_to_response("userinfo.html", {'form': form,'formPW':formPW},
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


import urllib2, urllib, hashlib, random
def send_smscode(request):
    phoneNum = request.POST.get('phoneNum', '')
    print phoneNum
    m = hashlib.md5()
    m.update('cs20150727')
    random_code = random.randint(1000, 9999)
    dict_code['smscode'] = random_code
    print "the random_code %s" % dict_code
    content = "您的验证码是：%s，有效期为五分钟。如非本人操作，可以不用理会"%random_code
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
           """ % ("cs20150727", m.hexdigest().upper(), int(phoneNum), content.decode("utf-8").encode("GBK"))
    print data
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    request = urllib2.Request(
                               url = r'http://userinterface.vcomcn.com/Opration.aspx',
                               headers= {'Content-Type':'text/xml'},
                               data = data
                              )
    print "send phone"
    print opener.open(request).read()

def index(request):
    return render_to_response('index.html',{}, context_instance=RequestContext(request))


def agreement(request):

    ag = RegistrationAgreement.objects.filter(name="registration_agreement")
    print "ag is :",ag
    return render_to_response('agreement.html',{'agreement':ag[2].agreement}, context_instance=RequestContext(request))


def index_zc(request):
    pj = Project.objects.filter(active=1)
    print pj
    return render_to_response('index_page.html',{}, context_instance=RequestContext(request))

def index_jf(request):
    pj = Project.objects.filter(active=1)
    print pj
    return render_to_response('home.html',{}, context_instance=RequestContext(request))

def about_us(request):
    p1 = RegistrationAgreement.objects.filter(name="mianzetiaokuan")
    p2 = About_us.objects.filter(name=u"上海辞达金融信息服务有限公司")
    return render_to_response('about.html',{"p1":p1[0].agreement,"description":p2[0].description}, context_instance=RequestContext(request))

def guide(request):
    p2 = About_us.objects.filter(name=u"关于众投")
    print p2
    return render_to_response('guide.html',{"description":p2[0].description}, context_instance=RequestContext(request))

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
    search_word = request.GET.getlist('search_word[]')
    print search_word
    if search_word == [u'1', u'4']:
        results = UserInformation.objects.all()
    elif search_word == [u'1', u'5']:
        results = UserInformation.objects.filter(cate=5)
    elif search_word == [u'1', u'6']:
        results = UserInformation.objects.filter(cate=6)
    elif search_word == [u'1', u'7']:
        results = UserInformation.objects.filter(cate=7)
    elif search_word == [u'1', u'8']:
        results = UserInformation.objects.filter(cate=8)
    elif search_word == [u'1', u'9']:
        results = UserInformation.objects.filter(cate=9)
    elif search_word == [u'1', u'10']:
        results = UserInformation.objects.filter(cate=10)
    elif search_word == [u'2', u'4']:
        results = UserInformation.objects.filter(authentication_class=2)
    elif search_word == [u'2', u'5']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=5)
    elif search_word == [u'2', u'6']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=6)
    elif search_word == [u'2', u'7']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=7)
    elif search_word == [u'2', u'8']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=8)
    elif search_word == [u'2', u'9']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=9)
    elif search_word == [u'2', u'10']:
        results = UserInformation.objects.filter(authentication_class=2).filter(cate=10)
    elif search_word == [u'3', u'4']:
        results = UserInformation.objects.filter(authentication_class=3)
    elif search_word == [u'3', u'5']:
        results = UserInformation.objects.filter(authentication_class=3).filter(cate=5)
    elif search_word == [u'3', u'6']:
        results = UserInformation.objects.filter(authentication_class=3).filter(cate=6)
    elif search_word == [u'3', u'7']:
        results = UserInformation.objects.filter(authentication_class=3).filter(cate=7)
    elif search_word == [u'3', u'8']:
        results = UserInformation.objects.filter(authentication_class=3).filter(cate=8)
    elif search_word == [u'3', u'9']:
        results = UserInformation.objects.filter(authentication_class=3).filter(cate=9)
    elif search_word == [u'3', u'10']:
       results = UserInformation.objects.filter(authentication_class=3).filter(cate=10)
    else:
        results = UserInformation.objects.all()
    print "xxxxxxxxxxxxxx"
    """
    for i in results:
        print "testxxxxx",i.realname,i.position,i.industry,i.user.username
        print dir(i.user)
        print "all leadertttttttttttttttttttttttttttt:%s"%i.user.manager_set.all().count()
        print "all investortttttttttttttttttttttttttttt:%s"%i.user.investor_set.all().count()
        p1=Project.objects.all()
        #print p1
        print dir(p1)
        print "xxxxxx"
        print dir(p1.leader)
        for i in p1:
             print dir(i)
             p2 =  p1.leader.filter(username = i.user.username)
             print "p2:%s"%p2
        #print "p1.count:%s"%p1.count
    """
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
    p = Project.objects.filter(id=objectid)
    print "p[0].leader",p[0].leader.all()
    return render_to_response('prodetails.html',{"project":p[0]}, context_instance=RequestContext(request))

def readmore(request,objectid):
    return render_to_response('readMore.html',{"objectid":objectid}, context_instance=RequestContext(request))

def search(request):
    #1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例
    search_word = request.GET.get('search_word[]',None)
    if search_word is not None:
        if int(search_word) == 2 :
            results = Project.objects.filter(active=0)
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

def search_zc(request):
    #1:不限，2：每日精选，3：预热中，4：众筹中，5：众筹成功，6：成功案例
    search_word = request.GET.get('search_word[]',None)
    if search_word is not None:
        if int(search_word) == 2 :
            results = Project.objects.filter(active=0)
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

    ppp = Paginator(results, 4)
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
    investor=u"%s"%objectid
    p1 = UserInformation.objects.filter(user=User.objects.filter(username=investor)[0])
    #print p1[0].realname, p1[0].position, p1[0].industry, p1[0].authentication_class
    return render_to_response('investor_intro.html',{"investor_info":p1[0]}, context_instance=RequestContext(request))

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