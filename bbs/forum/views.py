# -*- coding: utf-8 -*-
from bbs.account.models import profile
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.context_processors import csrf
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from ddbid import conf
from bbs.forum.models import topic, post, node, appendix, theme, topic_collect, mention
from bbs.account.models import user_collect, profile
from DjangoCaptcha import  Captcha
import json
import markdown
import operator
import random
# Create your views here.


def error(request, msg, back=None):
    return render_to_response('error.html', {'conf': conf, 'title': _('notice'),
                                             'msg': msg,
                                             'back': back,
                                             'request': request, })


def previewer(request):
    c = request.REQUEST['content']
    md = {}
    md['marked'] = markdown.markdown(c, ['codehilite'], safe_mode='escape')
    return HttpResponse(json.dumps(md))


def index(request):
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
    topics = topic.objects.all().filter(deleted=False).order_by('-last_replied')
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    post_list_title = _('latest topics')
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    print(mes)
    return render_to_response('forum/index.html', {'topics': topics, 'title': _('home'),
                                             'hot_topics': hot_topics,
                                             'essence_topic': essence_topic,
                                             'post_list_title': post_list_title,
                                             'theme1': theme1,
                                             'theme2': theme2,
                                             'theme3': theme3,
                                             'theme4': theme4,
                                             'collects': collects,
                                             'mes': mes,
                                             'user_collects': user_collects,
                                             'conf': conf},
                              context_instance=RequestContext(request))


def collected_view(request):
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
    collected = topic_collect.objects.all().filter(user_id=request.user.id, deleted=False).values('topic_id')
    ct = topic.objects.all().filter(id__in=collected)
    #topics = topic.objects.all().filter(deleted=False).order_by('-last_replied')
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    post_list_title = _('latest topics')
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    print(hot_topics)
    return render_to_response('forum/collect-view.html', {'topics': ct,
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
                                             'mes': mes,
                                             'conf': conf},
                              context_instance=RequestContext(request))


def topic_view(request, topic_id):
    t = topic.objects.get(id=topic_id)
    t.click += 1
    t.save()
    n = t.node
    posts = t.post_set.filter(deleted=False)
    try:
        page = request.GET['page']
    except:
        page = None
    if page == '1':
        page = None
    if topic_collect.objects.filter(topic_id=topic_id, user_id=request.user.id).exists():
        collected = topic_collect.objects.get(topic_id=topic_id, user_id=request.user.id).deleted
    else:
        collected = True
    #tc1 = topic_collect.objects.exists(topic_id=topic_id, user_id=request.user.id)
    theme1 = theme.objects.all().filter(id=1)
    theme2 = theme.objects.all().filter(id=2)
    theme3 = theme.objects.all().filter(id=3)
    theme4 = theme.objects.all().filter(id=4)
    conf.themes = theme.objects.all()
    conf.node1 = node.objects.filter(theme_id=1)
    conf.node2 = node.objects.filter(theme_id=2)
    conf.node3 = node.objects.filter(theme_id=3)
    conf.node4 = node.objects.filter(theme_id=4)
    this_theme = t.node.theme.id
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    return render_to_response('forum/topic.html', {'conf': conf, 'title': t.title,
                                             'request': request,
                                             'topic': t,
                                             'node': n,
                                             'collected': collected,
                                             'pager': page,
                                             'theme1': theme1,
                                             'theme2': theme2,
                                             'theme3': theme3,
                                             'theme4': theme4,
                                             'this_theme': this_theme,
                                             'hot_topics': hot_topics,
                                             'essence_topic': essence_topic,
                                             'collects': collects,
                                             'user_collects': user_collects,
                                             'mes': mes,
                                             'posts': posts},
                              context_instance=RequestContext(request))


def collect_topic(request, topic_id):
    print('collect_topic')
    print(request.user.id)
    t = topic.objects.get(id=topic_id)
    t.click -= 1
    t.save()

    if topic_collect.objects.filter(user_id=request.user.id, topic_id=topic_id).exists():
        tc = topic_collect.objects.get(topic_id=topic_id, user_id=request.user.id)
        if tc.deleted is True:
            tc.deleted = False
        else:
            tc.deleted = True
        tc.save()
    else:
        tc1 = topic_collect()
        tc1.topic_id = topic_id
        tc1.user_id = request.user.id
        tc1.deleted = False
        tc1.save()
    return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': topic_id}))

def verifycode(request):
    figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ca = Captcha(request)
    ca.words = [''.join([str(random.sample(figures, 1)[0]) for i in range(0, 4)])]
    ca.type = 'word'
    ca.img_width = 60
    ca.img_height = 20
    return ca.display()

def create_reply(request, topic_id):
    if request.method == 'POST':
        _code = request.POST.get('log_code')
        if not _code:
                return render_to_response('bbserror.html', {'error_message': '请输入验证码'})
        else:
            ca = Captcha(request)
            if ca.check(_code):
                t = topic.objects.get(id=topic_id)
                r = post()
                r.topic = t
                this_theme = t.node.theme.id
                if request.POST['content']:
                    r.content = request.POST['content']
                else:
                    return render_to_response('bbserror.html', {'error_message': '内容不能为空'})
                r.user = request.user
                r.content = r.content.replace("<img>", "<img class = 'bbs_reply_img' src='")
                r.content = r.content.replace("</img>", "'/>")
                r.content = r.content.replace("\r\n", "<br/>")
                r.save()
                return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t.id}))
            else:
                return render_to_response('bbserror.html', {'error_message': '验证码输入有误，请重新输入'})
    elif request.method == 'GET':
        return error(request, 'don\'t get')


def node_view(request, node_id):
    try:
        page = request.GET['page']
    except:
        page = None
    if page == '1':
        page = None
    n = node.objects.get(id=node_id)
    topics = topic.objects.filter(node=n, deleted=False)
    theme1 = theme.objects.all().filter(id=1)
    theme2 = theme.objects.all().filter(id=2)
    theme3 = theme.objects.all().filter(id=3)
    theme4 = theme.objects.all().filter(id=4)
    conf.node1 = node.objects.filter(theme_id=1)
    conf.node2 = node.objects.filter(theme_id=2)
    conf.node3 = node.objects.filter(theme_id=3)
    conf.node4 = node.objects.filter(theme_id=4)
    hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
    essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
    collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    return render_to_response('forum/node-view.html', {'request': request, 'title': n.title,
                                                 'conf': conf,
                                                 'topics': topics,
                                                 'node': n,
                                                 'node_view': True,
                                                 'theme1': theme1,
                                                 'theme2': theme2,
                                                 'theme3': theme3,
                                                 'theme4': theme4,
                                                 'node_id': node_id,
                                                 'theme_id': n.theme_id,
                                                 'hot_topics': hot_topics,
                                                 'essence_topic': essence_topic,
                                                 'user_collects': user_collects,
                                                 'collects': collects,
                                                 'mes': mes,
                                                 'pager': page, },
                              context_instance=RequestContext(request))
def node_list(request, theme_id):
    print(theme_id)
    n = theme.objects.get(id=theme_id)
    nodes = node.objects.filter(theme=n)
    print(nodes)
    conf.nodes = nodes
    conf.themes = theme.objects.all()
    conf.user_count = profile.objects.count()
    conf.topic_count = topic.objects.count()
    conf.post_count = post.objects.count()
    topics = topic.objects.all().filter(deleted=False).order_by('-last_replied')[0:30]
    hot_topics = topic.objects.all().filter(hot_flag=True)
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    post_list_title = _('latest topics')
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    return render_to_response('forum/index.html', {'topics': topics, 'title': _('home'),
                                             'hot_topics': hot_topics,
                                             'request': request,
                                             'post_list_title': post_list_title,
                                             'user_collects': user_collects,
                                             'mes': mes,
                                             'theme': n,
                                             'conf': conf})


def create_topic(request, node_id):
    n = node.objects.get(id=node_id)
    if request.method == 'GET':
        theme1 = theme.objects.all().filter(id=1)
        theme2 = theme.objects.all().filter(id=2)
        theme3 = theme.objects.all().filter(id=3)
        theme4 = theme.objects.all().filter(id=4)
        conf.themes = theme.objects.all()
        conf.node1 = node.objects.filter(theme_id=1)
        conf.node2 = node.objects.filter(theme_id=2)
        conf.node3 = node.objects.filter(theme_id=3)
        conf.node4 = node.objects.filter(theme_id=4)
        this_t = node.objects.get(id=node_id)
        this_theme = this_t.theme_id
        hot_topics = topic.objects.all().filter(hot_flag=True, deleted=False).order_by('-time_created')[0:4]
        essence_topic = topic.objects.all().filter(essence_flag=True, deleted=False).order_by('-time_created')[0:4]
        collects = topic_collect.objects.filter(user_id=request.user.id, deleted=False).count()
        user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
        mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
        return render_to_response('forum/create-topic.html', {'node': n, 'title': _('create topic'),
                                                        'node_view': True,
                                                        'theme1': theme1,
                                                        'theme2': theme2,
                                                        'theme3': theme3,
                                                        'theme4': theme4,
                                                        'request': request,
                                                        'hot_topics': hot_topics,
                                                        'essence_topic': essence_topic,
                                                        'collects': collects,
                                                        'user_collects': user_collects,
                                                        'this_theme': this_theme,
                                                        'mes': mes,
                                                        'conf': conf},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
            if not request.user.is_authenticated():
                        return error(request, '请登陆123', reverse('signin'))
            t = topic()
            t.content = request.POST.get('content') or ''
            t.content = t.content.replace("<img>", "<img class = 'bbs_topic_img' src='")
            t.content = t.content.replace("</img>", "'/>")
            t.content = t.content.replace("\r\n", "<br/>")
            t.node = n
            t.title = request.POST['title']
            _code = request.POST.get('log_code')
            if not t.title:
                #messages.add_message(request, messages.WARNING, _('title cannot be empty'))
                #return HttpResponseRedirect(reverse('create_topic', kwargs={'node_id': node_id}))
                return render_to_response('bbserror.html', {'error_message': '标题不能为空'})
            if not t.content:
                return render_to_response('bbserror.html', {'error_message': '内容不能为空'})
            if not _code:
                return render_to_response('bbserror.html', {'error_message': '请输入验证码'})
            else:
                ca = Captcha(request)
                if ca.check(_code):
                    t.user = request.user
                    t.save()
                    return HttpResponseRedirect(reverse('topic_view',
                                                        kwargs={'topic_id': t.id}))
                else:
                    return render_to_response('bbserror.html', {'error_message': '验证码输入有误，请更换验证码再次输入'})



def search(request, keyword):

    keys = keyword.split(' ')
    condition = reduce(operator.and_,
                       (Q(title__contains=x) for x in keys))
    topics = topic.objects.filter(condition)
    try:
        page = request.GET['page']
    except:
        page = None
    if page == '1':
        page = None
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
    return render_to_response('forum/index.html', {'request': request, 'title': _('%s-search result') % (keyword),
                                             'conf': conf, 'pager': page,
                                             'topics': topics,
                                             'theme1': theme1,
                                             'theme2': theme2,
                                             'theme3': theme3,
                                             'theme4': theme4,
                                             'hot_topics': hot_topics,
                                             'essence_topic': essence_topic,
                                             'collects': collects,
                                             'user_collects': user_collects,
                                             'mes': mes,
                                             'post_list_title': _('search %s') % (keyword), })


def recent(request):
    try:
        page = request.GET['page']
    except:
        page = None
    if page == '1':
        page = None
    topics = topic.objects.all().filter(deleted=False)
    return render_to_response('forum/index.html', {'request': request, 'title': _('latest topics'),
                                             'conf': conf,
                                             'topics': topics,
                                             'recent': 'reccent',
                                             'pager': page,
                                             'post_list_title': _('latest posted topics'), },
                              context_instance=RequestContext(request))


@staff_member_required
def del_reply(request, post_id):
    p = post.objects.get(id=post_id)
    t_id = p.topic.id
    p.deleted = True
    p.save()
    p.topic.save()
    return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t_id}))


def del_topic(request, topic_id):
    t = topic.objects.get(id=topic_id)
    if request.user != t.user and (not request.user.is_superuser):
        return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t.id}))
    n_id = t.node.id
    t.deleted = True
    t.save()
    return HttpResponseRedirect(reverse('node_view', kwargs={'node_id': n_id}))


def edit_topic(request, topic_id):
    t = topic.objects.get(id=topic_id)
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
    this_theme = t.node.theme.id
    user_collects = user_collect.objects.filter(user_id=request.user.id, deleted=False).count()
    mes = mention.objects.filter(receiver_id=request.user.id, read=False).count()
    if request.user != t.user and (not request.user.is_superuser):
        return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t.id}))
    if request.method == 'GET':
        return render_to_response('forum/edit-topic.html', {'request': request, 'conf': conf,
                                                     'theme1': theme1,
                                                     'theme2': theme2,
                                                     'theme3': theme3,
                                                     'theme4': theme4,
                                                     'hot_topics': hot_topics,
                                                     'essence_topic': essence_topic,
                                                     'collects': collects,
                                                     'topic': t,
                                                     'mes':mes,
                                                     'this_theme': this_theme,
                                                     'user_collects': user_collects,
                                                     'title': _('topic edit')},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        t.title = request.POST['title']
        t.content = request.POST['content']
        t.content = t.content.replace("\r\n", "<br/>")
        if not t.title:
            messages.add_message(request, messages.WARNING, _('title cannot be empty'))
            return HttpResponseRedirect(reverse('edit_topic', kwargs={'topic_id': t.id}))
        t.save()

        return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t.id}))


def add_appendix(request, topic_id):
    t = topic.objects.get(id=topic_id)
    n = t.node
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
    if request.user != t.user:
        return error(request, _('you cannot add appendix to other people\'s topic'))
    if request.method == 'GET':
        return render_to_response('forum/append.html', {'request': request, 'title': _('add appendix'),
                                                  'theme1': theme1,
                                                  'theme2': theme2,
                                                  'theme3': theme3,
                                                  'theme4': theme4,
                                                  'node': n, 'conf': conf,
                                                  'hot_topics': hot_topics,
                                                  'essence_topic': essence_topic,
                                                  'collects': collects,
                                                  'user_collects': user_collects,
                                                  'mes': mes,
                                                  'topic': t, },
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        a = appendix()
        a.content = request.POST['content']
        if not a.content:
            messages.add_message(request, messages.WARNING, _('content cannot be empty'))
            return HttpResponseRedirect(reverse('add_appendix', kwargs={'topic_id': t.id}))
        a.topic = t
        a.save()
        return HttpResponseRedirect(reverse('topic_view', kwargs={'topic_id': t.id}))


def node_all(request):
    nodes = {}
    nodes[u'分类1'] = list(theme.objects.filter(id__in=[1]).all())
    return render_to_response('forum/node-all.html', {'request': request, 'title': _('all nodes'),
                                                'conf': conf,
                                                'nodes': nodes, },
                              context_instance=RequestContext(request))

