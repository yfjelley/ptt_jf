# coding=utf-8
import random
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from searcher.models import RegistrationAgreement, About_us, Partners, Frendlink
from django.contrib.auth.models import User
from searcher.models import Bid, UserFavorite, Platform, UserInformation,Project
a = u"授权并附随本字库软件的复明。 1.1字库软算机软件、字体、说明书等印刷材料，以及光盘封套等包装材料（其他代理商、销售商等非方正电子公司自行印制的印刷材料及包装材料等除外）。本字库软件中所涉及的字库格式包括但不限于True type格式、Open type格式、PostScript Type 1、Type 0格式和CID格式。 1.2 美术作品说明 字库软件所实现的字是美术作品，因此您对该美术作品的使用要遵循《中华人民共和国著作权法》以及《中华人民共和国著作权法实施条例》有关规定。 2．定义。 2.1“用户”或“您”是指向方正电子公司许可的代理商或经销商购买正版软件产品复制件，并直接在计算机上安装、使用本字库软件及本字库软件所包含字体的自然人、法人或单一非法人组织。 用户应依照本协议安装、使用本字库软件及本字库软件所包含的字体。 2.2 “使用”是指安装、下载、复制、展览或以其他方式通过利用本字库软件的功能而获益的行为。 2.3 “授权数量”是指方正电子公司授予用户有效许可证的数量。如方正电子公司签属方正字库许可使用协议未另行指明，授权数量则为一件。 3．字库软件的使用。 如您从方正电子公司或其授权的代理商或经销商处取得字库软件，并且以您遵守本协议的条款为前提，方正电子公司即授予您以下关于本字库软件的非独占性许可，允许您按照本协议规定的如下用途使用本字库软件： 3.1安装使用：您仅可以在一台装有Windows或Mac OS的电子计算机上安装、运行本字库软件供个人非商业使用，不得在两台或两台以上的电子计算机设备上同时使用本字库软件； 3.2屏幕显示或输出：您可以将本字库软件所包含的字体用于屏幕显示；您也可以将通过本字库软件所生成的字形图像输出至与安装软件的计算机相连的设备上进行显示或打印，此类输出只能供您个人、非商业目的使用。 3.3备份：为防止复制品损坏您可以制作字库软件备份副本一份，该副本的使用范围与原复制品一致。 如果您的使用需求超出了本协议的使用许可范围，尤其是，您出于商业目的为他人而复制、发行或者展览了本协议中的知识产权，请与我们联系以获取方正字库知识产权的相应授权。 4．字库软件的使用限制。 4.1您不得对本字库软件进行复制、修改、仿制、反编译、反汇编、反向工程、转换、翻译、拆分，或以其他方式试图从本软件取得源代码，或从本软件文档中摘取其实质部分作其他应用； 4.2您不得单独或者附带地以出售、出租、出借等方式向公众发行或通过赠与、转让以及有线或者无线网络传播本字库软件； 4.3 您不得单独或者附带地将本字库软件及其所包含的字体提供给未经方正电子许可的第三人，使该第三人以向公众展览、展示、放映、表演等方式使用本字库软件及其字体，不论您的提供行为是出于商业目的还是非商业目的。 如果您在向公众做如下形式（包括但不限于）的发布时需要使用方正字体的，必须事先获得方正电子公司的书面授权许可： 4.3.1 将方正字体直接、格式转换或修改后用于企业名称、商标、标识； 4.3.2 将方正字体直接、格式转换或修改后用于企业宣传册； 4.3.3将方正字体直接、格式转换或修改后用于产品包装、附加标牌； 4.3.4将方正字体直接、格式转换或修改后用于产品说明书； 4.3.5将方正字体直接、格式转换或修改后用于发布卖场海报、平面广告、电视广告、户外广告、网络广告等； 4.3.6将方正字体直接、格式转换或修改后用于企业自有网站； 4.3.7将方正字体直接、格式转换或修改后用于发布音像制品、展览、展示中； 4.3.8其他应当由方正电子公司书面许可的情况。 4.4未经方正电子公司的书面许可，您不得将本字库软件的字型嵌入到可携式文件中（包括但不限于pdf、WORD等文件格式），亦不得将本软件使用于网络上及多用户环境。 4．5根据字库软件中字体的美术作品属性，如果您没有获得方正电子公司的明确的授权许可不得实施下述行为，包括但不限于：发表、署名、修改、复制、发行、出租、展览、放映、广播、信息网络传播、摄制、改编、翻译、汇编等。 4.6 其他依法应被禁止或者限制的行为。 5．知识产权。 本字库软件及其所包含的字体以及方正电子公司授权您制作的任何副本均为方正电子公司的知识产品（在本“字库软件”产品中另有知识产权声明的除外），本字库软件的结构、组织和代码以及与本字库软件相关的所有信息均为方正电子公司的商业秘密。本字库软件及其所包含的字体（即美术作品）受《中华人民共和国著作权法》、《计算机软件保护条例》和其他知识产权法律法规及国际公约、条约的保护。除本协议中明确的许可，方正电子公司不授予您对本字库软件其他的知识产权权利。本字库软件已经申请商标注册，因此禁止任何侵犯方正电子公司商标权的行为。 6．有限保证。 6.1在您遵守本协议条款的前提下，方正电子公司保证： (a) 本字库软件符合附随书面材料所述的功能； (b) 为您提供的支持服务与附随的书面材料中所述相符； 6.2 方正电子公司及其授权供应商对您所承担的全部责任，以及您所享有的所有补偿以下列两者之一为限： (a) 退还您购买不符合本协议第6.1条规定的字库软件产品时已支付的价款（如有）； (b) 修正或更换不符合本协议第6.1条规定的字库软件。经更换的字库软件产品的保证期限为原保证期剩余的期限或自更换日起计三十天（以时间较长者为准）。 进行索赔时，您必须在购得本字库软件后九十（90）天内、且仅在可提供购买本字库软件发票的情况下，向方正电子公司或其授权供应商提出。 6.3本字库软件因事故、不当使用或错误操作而造成无法使用的，不适用本协议的有限保证条款。 6.4前述有限保证规定了当方正电子公司或其授权供应商违反本协议第6.1条保证规定时的唯一和专有的赔偿方式。在适用法律所允许的最大范围内，方正电子公司及其授权供应商就本字库软件不做其他明示或默示的保证，其中包括（但不限于）对字库软件产品的适销性、适用性、所有权或无侵权的默示保证以及提供或未提供支持服务。 7．责任限制。 方正电子公司或其授权供应商在任何情况下都不对任何损失、索赔或费用或任何因果的、特殊的、意外的、间接的、惩罚性的或其他任何损失（包括但不限于利润损失、营业中断、商业信息的遗失或任何其他金钱上的损失）承担任何责任，也不对任何第三方的索赔或费用承担赔偿责任，即使方正电子公司或其授权供应商事先被告知该损害发生的可能性。不论任何情况，方正电子公司或其授权供应商依照本协议任何条款下所承担的全部责任，均限于您购买本软件产品所实际已付的价款（如果有的话）。但是，如果您已经与方正电子公司就授权许可使用达成书面协议，则方正电子公司的赔偿责任应以该协议条款为准。 8．许可终止。 一旦您违反本协议的条款，方正电子公司随时可能终止本协议、收回授权，并要求您承担相应法律责任。 9．适用法律与管辖。 本协议适用中华人民共和国的法律。 如您与方正电子公司就本字库软件的相关问题发生争议，您与方正电子公司均有权向北京市海淀区人民法院 提起诉讼。 1协议。"
def writeagreement(request):
    p1 = RegistrationAgreement.objects.all()
    p1.delete()
    p1 = RegistrationAgreement(name="regist_arg",agreement=a)
    p1.save()

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






