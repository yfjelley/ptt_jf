# coding=utf-8
import random
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from searcher.models import RegistrationAgreement, About_us, Partners, Frendlink
from django.contrib.auth.models import User
from searcher.models import Bid, UserFavorite, Platform, UserInformation,Project

def writeagreement(request):
    #p1 = RegistrationAgreement.objects.all()
    #p1.delete()
    #p1 = RegistrationAgreement(name="regist_arg",agreement=a)
    #p1.save()

    p1 = About_us(name="上海辞达金融信息服务有限公司", address="上海市闵行区沪闵路7866号莲花广场2号楼908室", hotline="400-000-0000", email="sys@pttjf.com")
    p1.save()
    name= ['明明','笨笨','芳芳','圆圆','大大','东东']
    position=['中国风险投资公司高级总裁','总裁','总经理']
    industry = ['软件服务', '通讯', '电子产品','教育培训','市场营销']
    username=random.randint(13521448969,13698766400)

    password = str(username)[2:8]
    realname = random.choice(name)
    position = random.choice(position)
    industry = random.choice(industry)

    new_user = User.objects.create_user(username=username, password=password)
    new_user.save()

    u = UserInformation(user=new_user, photo_url='/static/upload/default.png', abcdefg=password,realname =realname,position=position,industry=industry,authentication_class=1)
    u.save()

    user = User.objects.all()
    #print user
    user=UserInformation.objects.filter(authentication_class=1)

     #游客0 投资人1 资深投资人2 创业者3
    us = {0:u'游客',1:u'投资人',2:u'资深投资人',3:u'创业者'}
    #金融在线 0 电子商务1 医疗2 互联网3 社交4
    ind = {0:u'金融在线',1:u'电子商务',2:u'医疗',3:u'互联网',4:u'社交'}
    for i in user:
        #print i.user
        #print i.position
        #print i.user.username
        pr=Project(publish=i.user,name="众筹",founder="yang")
        pr.save()
        f = Project.objects.filter(founder="yang").filter(name__contains="筹")
        print "xxxxx",Project.objects.filter(founder="yang").filter(name__contains="筹").count()
        if f:
            print "ceshi chenggong"
        print len(f)
        print f[0].founder

    ui = UserInformation.objects.filter(authentication_class=2)
    for i in  ui:
        print i.user



    return render_to_response('test.html',{'user':user}, context_instance=RequestContext(request))






