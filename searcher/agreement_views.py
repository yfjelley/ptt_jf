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

    test= """&nbsp;&nbsp;&nbsp;&nbsp;鉴于，上海辞达金融信息服务有限公司（下称“葡萄藤金服”）通过其旗下网站葡萄藤金服（网址：www.pttjf.com及www.pttzc.com）和微信公众号、手机软件客户端等其他平台（合称“平台”），旨在为创业企业提供股权众筹融资和为投资人提供安全可靠的众筹创投服务。平台所涉及的所有事项，相关权利义务以及最终法律责任均由葡萄藤金服承担。
鉴于，为帮助投资人更好地理解平台相关股权众筹项目的风险，根据相关法律法规和《注册协议》其他配套制度、规则与协议的有关规定，特制定本《投资风险提示书》。
在投资人接受《注册协议》并注册成为平台用户时，表明投资人已充分知晓、理解和接受本《投资风险提示书》以及平台相关股权众筹项目的风险，并愿意自行承担相关风险。本《投资风险提示书》的全部条款属于《注册协议》的一部分。
请注意，本《投资风险提示书》将会不时进行更新，平台将会即时公告更新后的版本，敬请关注。一旦发生争议，《投资风险提示书》以最新的条款为准。"""
    #t=RegistrationAgreement(name="mianzetiaokuan",agreement=test)

    t=RegistrationAgreement(name="wind_control",agreement=test)
    t.save()
    t=RegistrationAgreement(name="fund_security",agreement=test)
    t.save()
    t=RegistrationAgreement(name="financial_supervision",agreement=test)
    t.save()
    t=RegistrationAgreement(name="technical_support",agreement=test)
    t.save()
    """



    p1 = About_us(name="上海辞达金融信息服务有限公司", address="上海市闵行区沪闵路7866号莲花广场2号楼908室", hotline="021-34222366",zip_code="211100", email="sys@pttjf.com")
    p1.save()
    p2 = About_us.objects.all()
    print p2[0].name
    for i in p2:
        print i.address,i.hotline
    """
    """

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
    """








