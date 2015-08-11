# coding=utf-8
import datetime
import random
from django import forms
from django.contrib.auth.models import User

__author__ = 'py'
from django.db import models, connection

#定义Platform数据库模型
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
#封装查询的语句
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
        desc = cursor.description #返回的是一个列表
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

#定义userinformation数据库模型
class UserInformation(models.Model):
    user = models.OneToOneField(User)
    photo_url = models.URLField(blank=True, null=True)
    nickname = models.CharField('昵称', max_length=30, blank=True, null=True)
    realname = models.CharField('真实姓名', max_length=20, blank=True, null=True)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, null=True, default='S')  # M/F
    birthday = models.DateField('生日', blank=True, null=True)
    cellphone = models.CharField('手机号码', max_length=11, blank=True, null=True)
    email = models.EmailField('邮箱地址', blank=True, null=True)
    city = models.CharField('居住城市', max_length=255,blank=True, null=True)
    address = models.CharField('居住地址', max_length=255, blank=True, null=True)
    education = models.CharField('学历', max_length=1, choices=ED_CHOICES, null=True, default=0)
    monthly_income = models.CharField('月收入', max_length=1, choices=INCOME_CHOICES, null=True, default=0)
    marriage = models.CharField('婚姻状况', max_length=1, choices=MARRIAGE_CHOICES, null=True, default=3)
    qq_num = models.CharField('QQ', max_length=30, blank=True, null=True)
    wechat_num = models.CharField('微信', max_length=30, blank=True, null=True)
    weibo_num = models.CharField('微博', max_length=30, blank=True, null=True)
    abcdefg = models.CharField(max_length=50, blank=True, null=True)
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

#定义ThirdLogin数据库模型
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
    Flag = models.CharField('WX', max_length=30, blank=True, null=True)
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

#定义UserFilter数据库模型
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

#定义周热点数据库模型（包括title，url,status，add_date,modify_date字段）
class WeekHotSpot(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    status = models.IntegerField()
    add_date = models.DateTimeField('添加时间', auto_now_add=True)
    modify_date = models.DateTimeField('编辑时间', auto_now=True)

class User(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)


