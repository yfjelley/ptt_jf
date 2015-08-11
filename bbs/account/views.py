# encoding=utf-8
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from bbs.account.models import profile, social

#from django.utils.translation import LANGUAGE_SESSION_KEY
from ddbid import conf
from bbs.forum.views import error
import json
import os
import urllib
import urllib2
import re
import random
import Image
from bbs.forum.models import theme, node, topic_collect, topic, post, mention
from bbs.account.models import user_collect
from django.db import connection
# Create your views here.

storage = FileSystemStorage(
    location=conf.UPLOAD_PATH,
    base_url='/static/upload/'
)

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\_]*$', 'Only alphanumeric characters and underscore are allowed.')


def collect_user(request, user_id):
    if user_collect.objects.filter(user_id=request.user.id, collected_user_id=user_id).exists():
        uc = user_collect.objects.get(user_id=request.user.id, collected_user_id=user_id)
        if uc.deleted is True:
            uc.deleted = False
        else:
            uc.deleted = True
        uc.save()
    else:
        uc1 = user_collect()
        uc1.collected_user_id = user_id
        uc1.user_id = request.user.id
        uc1.deleted = False
        uc1.save()
    return HttpResponseRedirect(reverse('user_info', kwargs={'user_id': user_id}))


def collected_user_view(request):
    theme1 = theme.objects.all().filter(id=1)
    theme2 = theme.objects.all().filter(id=2)
    theme3 = theme.objects.all().filter(id=3)
    theme4 = theme.objects.all().filter(id=4)
    conf.themes = theme.objects.all()
    conf.node1 = node.objects.filter(theme_id=1)
    conf.node2 = node.objects.filter(theme_id=2)
    conf.node3 = node.objects.filter(theme_id=3)
    conf.node4 = node.objects.filter(theme_id=4)
    conf.user_count = profile.objects.count()
    conf.topic_count = topic.objects.count()
    conf.post_count = post.objects.count()
    collected = user_collect.objects.all().filter(user_id=request.user.id, deleted=False).values("collected_user_id")
    user_topic = topic.objects.filter(user_id__in=collected)
    #user_topic = topic.objects.raw("select * from forum_topic where user_id in  (select collected_user_id from account_user_collect where deleted ='0' and user_id = %s ) order by time_created desc",[request.user.id])
    #topics = topic.objects.all().filter(deleted=False).order_by('-last_replied')
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    post_list_title = _('latest topics')
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    return render_to_response('forum/collect-user-view.html', {'users': collected,
                                             'hot_topics': hot_topics,
                                             'request': request,
                                             'essence_topic': essence_topic,
                                             'post_list_title': post_list_title,
                                             'theme1': theme1,
                                             'theme2': theme2,
                                             'theme3': theme3,
                                             'theme4': theme4,
                                             'collects': collects,
                                             'user_collects': user_collects,
                                             'topics': user_topic,
                                             'mes': mes,
                                             'conf': conf},
                              context_instance=RequestContext(request))

def user_info(request, user_id):
    uid = user_id
    u = User.objects.get(id=uid)
    theme1 = theme.objects.all().filter(id=1)
    theme2 = theme.objects.all().filter(id=2)
    theme3 = theme.objects.all().filter(id=3)
    theme4 = theme.objects.all().filter(id=4)
    conf.themes = theme.objects.all()
    conf.node1 = node.objects.filter(theme_id=1)
    conf.node2 = node.objects.filter(theme_id=2)
    conf.node3 = node.objects.filter(theme_id=3)
    conf.node4 = node.objects.filter(theme_id=4)
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    if not profile.objects.filter(user_id=u.id).exists():
        p = profile()
        p.user = u
        p.save()
    if user_collect.objects.filter(user_id=request.user.id, collected_user_id=user_id).exists():
        collected = user_collect.objects.get(user_id=request.user.id, collected_user_id=user_id).deleted
    else:
        collected = True
    return render_to_response('account/user-info.html', {'title': _('user info'),
                                                         'user1': u, 'conf': conf,
                                                         'topics': u.profile.latest_activity()['topic'],
                                                         'theme1': theme1,
                                                         'theme2': theme2,
                                                         'theme3': theme3,
                                                         'theme4': theme4,
                                                         'mes': mes,
                                                         'hot_topics': hot_topics,
                                                         'essence_topic': essence_topic,
                                                         'collects': collects,
                                                         'collected': collected,
                                                         'user_collects': user_collects,
                                                         'post_list_title': _('%s\'s topics') % (u.profile.username())},
                              context_instance=RequestContext(request))


def reg(request):
    if request.method == 'GET':
        return render_to_response('account/reg.html', {'conf': conf, 'title': _('register')},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        try:
            alphanumeric(username)
        except:
            messages.add_message(request, messages.WARNING,
                                 _('username can only contain letters digits and underscore'))
            return HttpResponseRedirect(reverse('reg'))

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, _('username already exists'))
            return HttpResponseRedirect(reverse('reg'))

        if password != password2 or password == '' or password2 == '':
            messages.add_message(request, messages.WARNING, _('passwords don\'t match, or are blank'))
            return HttpResponseRedirect(reverse('reg'))

        user = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(request, user)
        p = profile()
        p.user = user
        p.avatar_url = '/static/upload/default.png'
        p.save()
        return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'GET':
        return render_to_response('account/reg.html', {'conf': conf, 'title': _('sign in')},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, _('username does not exist'))
            return HttpResponseRedirect(reverse('signin'))

        if user is None:
            messages.add_message(request, messages.WARNING, _('password is invalid'))
            return HttpResponseRedirect(reverse('signin'))

        login(request, user)
        return HttpResponseRedirect(reverse('index'))


def setting(request):
    if request.method == 'GET':
        return render_to_response('account/user-setting.html', {'request': request,
                                                                'conf': conf,
                                                                'title': _('settings')},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        #request.user.profile.website = request.POST['website']
        request.user.email = request.POST['email']
        #request.user.profile.save()
        request.user.save()
        return render_to_response('account/user-setting.html', {'request': request,
                                                                'conf': conf,
                                                                'title': _('settings')},
                                  context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def view_mention(request):
    new = ''
    if mention.objects.filter(receiver_id=request.user.id).exists():
        new = mention.objects.filter(read=False, receiver_id=request.user.id)
        #new = request.user.received_mentions.filter(read=False)

    theme1 = theme.objects.all().filter(id=1)
    theme2 = theme.objects.all().filter(id=2)
    theme3 = theme.objects.all().filter(id=3)
    theme4 = theme.objects.all().filter(id=4)
    conf.themes = theme.objects.all()
    conf.node1 = node.objects.filter(theme_id=1)
    conf.node2 = node.objects.filter(theme_id=2)
    conf.node3 = node.objects.filter(theme_id=3)
    conf.node4 = node.objects.filter(theme_id=4)
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    for m in new:
        m.read = True
        m.save()
    return render_to_response('account/user-mention.html', {'request': request, 'title': _('mentions'),
                                                            'conf': conf,
                                                            'new': new,
                                                            'theme1': theme1,
                                                            'theme2': theme2,
                                                            'theme3': theme3,
                                                            'theme4': theme4,
                                                            'hot_topics': hot_topics,
                                                            'essence_topic': essence_topic,
                                                            'collects': collects,
                                                            'user_collects': user_collects,
                                                            'messages': messages,
                                                            'mes': mes, },
                              context_instance=RequestContext(request))


def change_password(request):
    u = request.user
    if request.method == 'GET':
        return render_to_response('account/change-password.html', {'request': request, 'title': _('change password'),
                                                                   'conf': conf},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        old = request.POST['old-password']
        new = request.POST['password']
        if request.POST['password'] != request.POST['password2'] or request.POST['password'] == '' or request.POST[
            'password2'] == '':
            messages.add_message(request, messages.WARNING, _('passwords don\'t match, or are blank'))
            return HttpResponseRedirect(reverse('change_password'))

        if authenticate(username=u.username, password=old):
            u.set_password(new)
            u.save()
            messages.add_message(request, messages.SUCCESS, _('password updated successfully'))
            return HttpResponseRedirect(reverse('change_password'))
        else:
            messages.add_message(request, messages.WARNING,
                                 _('unable to change your password, the current password may be invalid'))
            return HttpResponseRedirect(reverse('change_password'))


def user_avatar(request):
    u = request.user
    if request.method == 'GET':
        return render_to_response('account/user-avatar.html', {'request': request, 'title': _('avatar setting'),
                                                               'conf': conf},
                                  context_instance=RequestContext(request))
    else:
        #use_gravatar = request.POST.getlist('gravatar') == ['true']
        #request.user.profile.use_gravatar = use_gravatar
        f = request.FILES.get('file', None)
        print(f)
        if f:
            extension = os.path.splitext(f.name)[-1]
            if f.size > 524288:
                return error(request, _('file too big'))
            if (extension not in ['.jpg', '.png', '.gif']) or ('image' not in f.content_type):
                return error(request, _('file type not permitted'))
            im = Image.open(f)
            im.thumbnail((120, 120))
            name = storage.get_available_name(str(u.id)) + '.png'
            #print(storage.url(name))
            url = storage.url(name)
            #u.profile.avatar_url = url
            #request.profile.avatar_url = url
            #request.user.profile.avatar_url = url
            p = profile()
            if not profile.objects.filter(user_id=u.id).exists():
                p.user = u
                p.avatar_url = url
                im.save('%s/%s' % (storage.location, name), 'PNG')
        #u.profile.save()
            else:
                p = profile.objects.get(user_id=u.id)
                p.avatar_url = url
                im.save('%s/%s' % (storage.location, name), 'PNG')
            p.save()
        return HttpResponseRedirect(reverse('user_avatar'))


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='account/reset-password-confirm.html',
                                  uidb64=uidb64, token=token, post_reset_redirect=reverse('signin'))


def reset(request):
    return password_reset(request, template_name='account/reset-password.html',
                          email_template_name='account/reset-password-email.html',
                          subject_template_name='account/reset-password-subject.txt',
                          post_reset_redirect=reverse('signin'))


#def set_lang(request):
#    # the lang_code must be in the LANGUAGES tuple
#    if request.method == 'GET':
#        lang_code = request.GET['lang']
#        if hasattr(request, 'session'):
#            request.session[LANGUAGE_SESSION_KEY] = lang_code
#        else:
#            pass
#            #response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
#            #                    max_age=settings.LANGUAGE_COOKIE_AGE,
#            #                    path=settings.LANGUAGE_COOKIE_PATH,
#            #                    domain=settings.LANGUAGE_COOKIE_DOMAIN)
#        return HttpResponseRedirect(request.META['HTTP_REFERER'])

###############
#oauth related#
###############
def GenerateUsername(nickname):
    i = 0
    MAX = 999
    while (i < MAX):
        username = nickname + '__qq__' + str(random.randint(0, MAX))
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
    raise Exception('All random username are taken')


def qq_oauth(request):
    if request.method == 'GET':
        if (not request.GET['code']) or (request.GET['state'] != 'fairybbs'):
            return error(request, '请求错误')
        code = request.GET['code']
        url = 'https://graph.qq.com/oauth2.0/token'
        data = {'grant_type': 'authorization_code',
                'client_id': '',
                'client_secret': '',
                'code': code,
                'redirect_uri': ''}
        req = urllib2.Request(url, urllib.urlencode(data))
        res = urllib2.urlopen(req)
        try:
            access_token = re.findall(r'access_token=(.*?)&', res.read())[0]
        except:
            return error(request, u'抱歉，未从腾讯获取到有效的授权信息，可能是和腾讯通信失败，请重试\n')
        url_openid = 'https://graph.qq.com/oauth2.0/me'
        data_openid = {'access_token': access_token}
        req_openid = urllib2.Request(url_openid, urllib.urlencode(data_openid))
        res_openid = urllib2.urlopen(req_openid)
        try:
            JSON_openid = json.loads(res_openid.read()[10:-3])
        except:
            return error(request, u'抱歉，未从腾讯获取到有效的授权信息，可能是和腾讯通信失败，请重试')
        openid = JSON_openid['openid']
        try:
            u = social.objects.get(openid=openid).user
        except:
            url_info = 'https://graph.qq.com/user/get_user_info'
            data_info = {'oauth_consumer_key': '',
                         'access_token': access_token,
                         'openid': openid}
            req_info = urllib2.Request(url_info, urllib.urlencode(data_info))
            res_info = urllib2.urlopen(req_info)
            JSON_info = json.loads(res_info.read())
            username = JSON_info['nickname']
            nickname = username
            if JSON_info['figureurl_qq_2']:
                avatar = JSON_info['figureurl_qq_2']
            else:
                avatar = JSON_info['figureurl_2']
            password = User.objects.make_random_password()
            try:
                u = User.objects.get(username=username)
            except:
                pass
            else:
                username = GenerateUsername(nickname)
            u = User(username=username)
            u.set_password(password)
            u.save()
            p = profile(user=u,
                        #avatar=avatar,
                        nickname=nickname,
                        avatar_url=avatar,
                        use_gravatar=False)
            p.save()
            s = social(user=u,
                       access_token=access_token,
                       openid=openid,
                       avatar=avatar, )
            s.save()
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))  #login succeed
        else:
            u.social.access_token = access_token
            u.social.save()
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            if u is not None and u.is_active:
                auth.login(request, u)
                return HttpResponseRedirect(reverse('index'))  #login succeed
            else:
                return error(request, u'授权失败，请重试')
