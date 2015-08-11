from django.conf.urls import patterns, include, url

urlpatterns = patterns('bbs.account.views',
    url(r'^(?P<user_id>\d+)/info/$', 'user_info', name='user_info'),
    url(r'^reg/$', 'reg', name='reg'),
    url(r'^signin/$', 'user_login', name='signin'),
    url(r'^setting/$', 'setting', name='user_setting'),
    url(r'^signout/$', 'user_logout', name='signout'),
    url(r'^mention/$', 'view_mention', name='mention'),
    url(r'^oauth/qq/$', 'qq_oauth', name='qq_oauth'),
    url(r'password/$', 'change_password', name='change_password'),
    url(r'^avatar/$', 'user_avatar', name='user_avatar'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'reset_confirm', name='password_reset_confirm'),
    url(r'^reset/$', 'reset', name='password_reset'),
    url(r'^collect-user/(?P<user_id>\d+)/$', 'collect_user', name='collect_user'),
    url(r'collected-user-view/$', 'collected_user_view', name='collected_user_view'),
#    url(r'^set_lang/$', 'set_lang', name='set_lang'),
)
