# coding=utf-8
import datetime
import random
from django import forms
from django.contrib.auth.models import User

__author__ = 'py'
from django.db import models, connection


class Platform(models.Model):
    name = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    income_range = models.CharField(max_length=255, blank=True)
    term_range = models.CharField(max_length=255, blank=True)
    corporate = models.CharField(max_length=255, blank=True)
    capital = models.IntegerField(max_length=255, blank=True)
    online_time = models.DateField(blank=True, null=True)
    background = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    management_fee = models.CharField(max_length=255, blank=True)
    transfer_claim = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    pay_type = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=255, blank=True)
    valid_status = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_platform'

class BidManager(models.Manager):
    def comb_bid(self, amount):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT a.id as ida,
	    a.term as terma,
	    a.income_rate as incomea,
        a.amount as amounta,
	    b.id idb,
	    b.term as termb,
	    b.income_rate as incomeb,
        b.amount as amountb,
	    a.amount + b.amount as totalamount
        FROM yqdDB.searcher_bid a
        left join yqdDB.searcher_bid b
        on a.id <> b.id
        and b.process < 100
        where a.amount * a.process + b.amount * b.process <= %s
        and a.process < 100
        order by a.amount * a.process + b.amount * b.process desc """, [amount])
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


class Bid(models.Model):
    platform = models.ForeignKey(Platform)
    link = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    income_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    term = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    transfer_claim = models.CharField(max_length=255, blank=True)
    repay_type = models.CharField(max_length=255, blank=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    reward = models.CharField(max_length=255, blank=True)
    protect_mode = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    process = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField()
    month_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    allow_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    finish_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    ten_thousand_revenue = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    random_rank = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    term_name = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    term_unit = models.CharField(max_length=255, blank=True)
    objects = BidManager()

    class Meta:
        managed = False
        db_table = 't_subject'


class BidHis(models.Model):
    platform = models.ForeignKey(Platform)
    link = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    income_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    term = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    transfer_claim = models.CharField(max_length=255, blank=True)
    repay_type = models.CharField(max_length=255, blank=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    reward = models.CharField(max_length=255, blank=True)
    protect_mode = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    process = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField()
    month_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    allow_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    finish_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    ten_thousand_revenue = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    random_rank = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    term_name = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    term_unit = models.CharField(max_length=255, blank=True)
    objects = BidManager()

    class Meta:
        managed = False
        db_table = 't_subject_his'


class UserFavoriteManager(models.Manager):
    def my_favorite(self, userid):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT b.* FROM   searcher_userfavorite a
            left join searcher_bid b
            on b.id = a.id
            where a.id  =  %s""", [userid])
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


class UserFavorite(models.Model):
    user = models.ForeignKey(User)
    favorite_type = models.IntegerField()  # 1:bid 2:platform
    favorite_id = models.IntegerField()
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    fields = ('id', 'user_id', 'favorite_type', 'favorite_id', 'add_date', 'modify_date')
    objects = UserFavoriteManager()


GENDER_CHOICES = (
    ('M', '男'),
    ('F', '女'),
    ('S', '保密'),
)

ED_CHOICES = (
    ('0', '---'),
    ('1', '小学及以下'),
    ('2', '初中'),
    ('3', '高中'),
    ('4', '大专'),
    ('5', '本科'),
    ('6', '硕士'),
    ('7', '博士'),
)

INCOME_CHOICES = (
    ('0', '---'),
    ('1', '1000以内'),
    ('2', '1000-5000'),
    ('3', '5001-10000'),
    ('4', '10001-30000'),
    ('5', '30000以上'),
)

MARRIAGE_CHOICES = (
    ('1', '已婚'),
    ('2', '未婚'),
    ('3', '保密'),
)
AUTH_CLASS_CHOICES = (
    ('1', '认证投资人'),
    ('2', '认证资深投资人'),
    ('3', '认证领投人'),
    ('4', '认证资深领投人'),
)

INDUSTRY_CHOICE = (
    ('1', '金融在线'),
    ('2', '电子商务'),
    ('3', '医疗'),
    ('4', '互联网'),
    ('5', '社交'),
    ('6', '生活服务'),
)
CAT_CHOICE = (
    ('1', '金融在线'),
    ('2', '电子商务'),
    ('3', '医疗'),
    ('4', '互联网'),
    ('5', '社交'),
    ('6', '生活服务'),
)

CATEGORY_CHOICE = (
    ('1', '金融在线'),
    ('2', '电子商务'),
    ('3', '医疗'),
    ('4', '互联网'),
    ('5', '社交'),
    ('6', '生活服务'),
)
INVEST_TYPE_CHOICES =(
    ('1', '领投'),
    ('2', '跟投'),
)
class UserInformation(models.Model):
    user = models.OneToOneField(User)
    photo_url = models.CharField("照片",max_length=30,blank=True, null=True)
    nickname = models.CharField('昵称', max_length=30, blank=True, null=True)
    realname = models.CharField('真实姓名', max_length=20, blank=True, null=True)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, null=True, default='S')  # M/F
    birthday = models.DateField('生日', blank=True, null=True)
    cellphone = models.CharField('手机号码', max_length=11, blank=True, null=True)
    email = models.EmailField('邮箱地址', blank=True, null=True)
    city = models.CharField('居住城市', max_length=255,blank=True, null=True)
    address = models.CharField('居住详细地址', max_length=255, blank=True, null=True)
    education = models.CharField('学历', max_length=1, choices=ED_CHOICES, null=True, default=0)
    school = models.CharField('毕业学校', max_length=255, blank=True, null=True)
    education_experience = models.TextField('教育经历',blank=True,null=True)
    investment_case = models.TextField('投资案例',blank=True,null=True)
    basic_information = models.TextField('基本信息',blank=True,null=True)
    interests = models.TextField('兴趣爱好',blank=True,null=True)
    position = models.CharField('职位', max_length=255, blank=True, null=True)
    work_experience = models.TextField('工作经历', blank=True, null=True)
    monthly_income = models.CharField('月收入', max_length=1, choices=INCOME_CHOICES, null=True, default=0)
    marriage = models.CharField('婚姻状况', max_length=1, choices=MARRIAGE_CHOICES, null=True, default=3)
    qq_num = models.CharField('QQ', max_length=30, blank=True, null=True)
    wechat_num = models.CharField('微信', max_length=30, blank=True, null=True)
    weibo_num = models.CharField('微博', max_length=30, blank=True, null=True)
    abcdefg = models.CharField(max_length=50, blank=True, null=True)
    authentication_class = models.CharField('认证类别', max_length=1,choices=AUTH_CLASS_CHOICES, blank=True, null=True)
    id_card = models.CharField('身份证', max_length=255, blank=True, null=True)
    business_card = models.CharField('名片', max_length=255, blank=True, null=True)
    financial_assets = models.CharField('营业执照', max_length=255, blank=True, null=True)
    fixed_assets = models.CharField('组织机构代码', max_length=255, blank=True, null=True)
    income_assets = models.CharField('税务登记证', max_length=255, blank=True, null=True)
    ideas = models.TextField('投资理念',blank=True, null=True)
    direction = models.TextField('投资方向', blank=True, null=True)
    industry = models.CharField('关注的行业', max_length=1,choices=INDUSTRY_CHOICE, blank=True, null=True)
    attention_persion = models.ManyToManyField(User, related_name = "attention_persion_set",blank=True, null=True)#关注他的人
    fans = models.ManyToManyField(User, related_name = "fans_set",blank=True, null=True)#他的粉丝
    cate = models.CharField('行业类别', max_length=1,choices=CAT_CHOICE,blank=True, null=True)#所在行业
    link = models.URLField('推广链接', max_length=255, blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    login_times = models.IntegerField('登录次数', blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.user

class Project(models.Model):
    publish = models.ForeignKey(User,related_name = "publish_set", blank=True, null=True)#项目发布者 可以发布多个项目
    founder =models.TextField('项目创始人介绍',blank=True, null=True)#项目可以有多个创始人
    team = models.TextField('项目团队介绍',blank=True, null=True)#项目团队一个项目有多个成员
    leader = models.ManyToManyField(User, related_name = "manager_set",blank=True, null=True)#只能有一个领投人
    investor = models.ManyToManyField(User, related_name = "investor_set",blank=True, null=True)#跟投人
    click = models.ManyToManyField(User, related_name = "click_set",blank=True, null=True)#关注该项目的人
    collection = models.ManyToManyField(User, related_name = "collection_set",blank=True, null=True)#收藏该项目的人
    name = models.CharField('项目名称',max_length=255, blank=True, null=True)#项目名称
    logo = models.CharField('项目标志',max_length=255, blank=True, null=True)#项目标志
    photo_url = models.CharField('项目宣传图片',max_length=255, blank=True, null=True)#项目宣传图片
    introduction = models.TextField('项目简介',blank=True, null=True)#项目简介
    description = models.TextField('项目描述',blank=True, null=True)#项目描述
    category = models.CharField('行业类别',max_length=1,choices=CATEGORY_CHOICE, blank=True, null=True)#行业类别
    amount = models.CharField('融资总额',max_length=255, blank=True, null=True)#融资总额
    leader_inv_min = models.CharField('领投最低投资金额',max_length=255, blank=True)#领头最低投资额
    inv_min = models.CharField('跟投最低投资金额',max_length=255, blank=True)#跟头最低投资额
    invest_amount = models.CharField('每股金额',max_length=255, blank=True, null=True)#投资金额
    invest_num = models.CharField('股数',max_length=255, blank=True, null=True)#份数
    finish = models.CharField('已完成融资金额',max_length=255, blank=True, null=True)#已完成融资金额
    fund_use = models.TextField('资金用途',blank=True, null=True)#资金用途
    transfer_equity = models.CharField('出让股份',max_length=255, blank=True, null=True)#出让的股权份额
    company = models.CharField('注册公司',max_length=255, blank=True, null=True)#注册公司
    url = models.URLField('公司链接',max_length=255, blank=True, null=True)#公司链接
    other = models.CharField('其他信息',max_length=255, blank=True, null=True)#其他信息
    patent = models.TextField('专利',blank=True, null=True)#专利
    business_plan_url = models.CharField('商业计划书',max_length=255, blank=True, null=True)#商业计划书
    active = models.IntegerField('是否是精选',blank=True, null=True)#是否是精选
    status = models.IntegerField('进行到什么程度',blank=True, null=True)#进行到什么程度
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    Preheat_date = models.DateTimeField('预热时间',blank=True, null=True) #预热时间
    preheat_end_date = models.DateTimeField('预热结束时间',blank=True, null=True)#预热结束时间
    crowd_date = models.DateTimeField('众筹开始时间',blank=True, null=True)#众筹开始时间
    crowd_end_date = models.DateTimeField('众筹结束时间',blank=True, null=True)#众筹结束时间

    class Meta:
        db_table = 't_project'
    def __unicode__(self):
        return u'%s' % self.name

class invest_detail(models.Model):
    invest_user = models.ForeignKey(User,related_name = "invest_user_set", blank=True, null=True)
    invest_project = models.ForeignKey(Project,related_name = "invest_project_set", blank=True, null=True)
    invest_amount = models.CharField('每股金额',max_length=255, blank=True, null=True)#投资金额
    invest_num = models.CharField('股数',max_length=255, blank=True, null=True)#投资金额
    invest_type = models.CharField('领投or跟投',max_length=1,choices=INVEST_TYPE_CHOICES, blank=True, null=True)#领投or跟投
    time_created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.invest_user

class project_forum(models.Model):
    forum_user = models.ForeignKey(User,related_name = "forum_user_set", blank=True, null=True)
    forum_project = models.ForeignKey(Project,related_name = "forum_project_set", blank=True, null=True)
    forum_content = models.CharField(max_length=255, blank=True, null=True)#内容
    time_created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.forum_user

class Signal(models.Model):
    type = models.IntegerField(default=0)        # 0,系统公告；1:评论;2:私信;3.关注;4.主题关注
    obj = models.IntegerField(default=0)         # 对象id
    user = models.ForeignKey(User,related_name = "signal_user_set", blank=True, null=True)      # 发布者
    who = models.ForeignKey(User,related_name = "signal_who_set", blank=True, null=True)                   # 接受者
    title = models.CharField('标题',max_length=200, null=True)        # 标题
    content = models.TextField('内容', null=True)        # 内容
    status = models.IntegerField('状态',default=0)             # 状态，0，未读；1已读，2.删除
    add_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_signal'
    def __unicode__(self):
        return u'%s' % self.title

class ThirdLogin(models.Model):
    userInfo = models.OneToOneField(UserInformation)
    openId = models.CharField('平台验证', max_length=100, blank=True, null=True)
    accessToken = models.CharField('访问秘钥', max_length=100, blank=True, null=True)
    wxopenId = models.CharField('wx开放平台验证', max_length=100, blank=True, null=True)
    wxopenId2 = models.CharField('wx公众平台验证', max_length=100, blank=True, null=True)
    wxaccessToken = models.CharField('wx访问秘钥', max_length=200, blank=True, null=True)
    wbId = models.CharField('平台验证', max_length=100, blank=True, null=True)
    qqFlag = models.CharField('QQ', max_length=30, blank=True, null=True)
    wbFlag = models.CharField('WB', max_length=30, blank=True, null=True)
    wxFlag = models.CharField('WX开放平台用户', max_length=30, blank=True, null=True)
    wxFlag2 = models.CharField('WX公众平台用户', max_length=30, blank=True, null=True)
    wxBlock = models.CharField('微信用户退订记录', max_length=30, blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

class WXAccessToken(models.Model):
    accessToken = models.CharField('访问秘钥', max_length=1000, blank=True, null=True)
    expiresIn = models.IntegerField('time', max_length=30, blank=True, null=True)
    flag = models.CharField('WX', max_length=30, blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

class RemindQueue(models.Model):
    userId = models.IntegerField('userid', max_length=30, blank=True, null=True)
    subjectId = models.IntegerField('bid', max_length=30, blank=True, null=True)
    type = models.CharField('remind type', max_length=5, blank=True, null=True)
    bEndDate = models.DateTimeField('subject end time', blank=True, null=True)
    limit = models.CharField('remind limit', max_length=30, blank=True, null=True)
    remindDate = models.DateTimeField('remind date', blank=True, null=True)
    remindEndDate = models.DateTimeField('remind end date', blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    messageId = models.CharField('messageId', max_length=30, blank=True, null=True)
    flag = models.CharField('data flag', max_length=5, blank=True, null=True)


class FilterDimension(models.Model):
    dimensionname = models.CharField('维度名称', max_length=20)
    type = models.IntegerField('显示类型')
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    fields = ('id', 'dimensionname', 'add_date', 'modify_date')

    def __unicode__(self):
        return u'%s' % self.dimensionname


class DimensionChoice(models.Model):
    dimension = models.ForeignKey(FilterDimension)
    choice_name = models.CharField(max_length=20)
    choice_value1 = models.DecimalField(decimal_places=2, max_digits=16)
    choice_value2 = models.DecimalField(decimal_places=2, max_digits=16)
    cal_type = models.IntegerField()  # 1:<=  2:=  3:>= 4:between
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    fields = ('id', 'dimension', 'choice_name', 'choice_value1', 'choice_value2', 'cal_type', 'add_date', 'modify_date')

class UserFilter(models.Model):
    user = models.ForeignKey(User)
    filter_order = models.IntegerField()
    name = models.CharField(max_length=50, blank=True, null=True)
    choices = models.CharField(max_length=50)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    fields = ('id', 'user', 'filter_order', 'choice_yr', 'choice_tm', 'add_date', 'modify_date')


class ReminderUnit(models.Model):
    name = models.CharField(max_length=30)
    type = models.IntegerField('类型')  # 1:<=  2:=  3:>= 4:between
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)


class UserReminder(models.Model):
    user = models.ForeignKey(User)
    bid_id = models.IntegerField()
    reminder = models.ForeignKey(ReminderUnit)
    value = models.IntegerField()
    status = models.IntegerField('状态')  # 0 = invalid
    is_reminded = models.IntegerField('是否已提醒', default=0)  # 0 = 未提醒
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)


class platform_info_daily(models.Model):
    day_id = models.DateField()
    platform = models.ForeignKey(Platform)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    inv_quantity = models.DecimalField(decimal_places=2, max_digits=16)


class CombBidType(models.Model):
    name = models.CharField(max_length=50)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)


class WeekHotSpot(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    status = models.IntegerField()
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

class RegistrationAgreement(models.Model):
    name = models.CharField(max_length=50)
    agreement = models.TextField()
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name




class About_us(models.Model):
    name = models.CharField('公司名称',max_length=255, blank=True, null=True)#名称(公司，关于众筹)
    description = models.TextField('公司简介')#公司简介
    zip_code = models.CharField('邮编',max_length=255, blank=True, null=True)
    address = models.CharField('地址',max_length=255, blank=True, null=True)
    hotline = models.CharField('热线',max_length=255, blank=True, null=True)
    email  = models.EmailField( '邮箱',blank=True, null=True)
    about_zhongtou = models.TextField('关于众投', blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.name


class Partners(models.Model):
    name = models.CharField('公司名称',max_length=255, blank=True, null=True)#公司名称
    url = models.URLField('网址',max_length=255, blank=True, null=True)#网址
    active_status = models.IntegerField('状态',blank=True, null=True)#活跃状态
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)
    def __unicode__(self):
        return u'%s' % self.name


class Frendlink(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)#公司名称
    url = models.URLField(max_length=255, blank=True, null=True)#网址
    active_status = models.IntegerField(blank=True, null=True)#活跃状态
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

class AuthLogin(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    http_host = models.CharField('http_host', max_length=30, blank=True, null=True)
    http_referer = models.CharField('http_host', max_length=30, blank=True, null=True)
    remote_addr = models.CharField('remote_addr', max_length=30, blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)



