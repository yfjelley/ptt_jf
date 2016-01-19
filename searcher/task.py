# encoding:utf-8

from django.core.mail import send_mail
from celery import task, platforms

platforms.C_FORCE_ROOT = True

@task()
def sendmail(username,name,inv):
    print "sendmail"
    send_mail(
    u"葡萄藤预约投资通知",
    u"用户%s预约投资项目%s%s万份"%(username,name,inv),
    'service@ddbid.com',
    ['yangfeng@ddbid.com','fred.he@ddbid.com','james.lee@ddbid.com','amy.gu@ddbid.com','roger.wang@ddbid.com'],
    )

@task()
def add(x, y):
    return x + y