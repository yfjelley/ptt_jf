from django.conf.urls import patterns, url

urlpatterns = patterns('searcher.views',
    #url(r'^$', 'index', name='index'),
    url(r'^zc$', 'index_zc', name='index_zc'),
    url(r'^search_zc$', 'search_zc', name='search_zc'),
    url(r'^$', 'index_jf', name='index_jf'),
    url(r'^login/$',  'login', name='login'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^register/$',  'register', name='register'),
    url(r'^userinfo/$',  'userinfo', name='userinfo'),
    url(r'getverifycode/$', 'verifycode', name='verifycode'),
    url(r'forgetpw/$', 'forgetpw', name='forgetpw'),
    url(r'intermediary/(?P<objectid>\d+)/$', 'intermediary', name='intermediary'),

    url(r'^agreement/$',  'agreement', name='agreement'),
    url(r'^guide/$',  'guide', name='guide'),
    url(r'^about_us/$',  'about_us', name='about_us'),
    url(r'^investor/$',  'investor', name='investor'),
    url(r'^search_investor/$',  'search_investor', name='search_investor'),
    url(r'^safety/(?P<objectid>\d+)/$',  'safety', name='safety'),
    url(r'^investor_info/(?P<objectid>\d+)/$',  'investor_info', name='investor_info'),
    url(r'^contact_us/$',  'contact_us', name='contact_us'),
    url(r'^prodetails/(?P<objectid>\d+)/$',  'prodetails', name='prodetails'),

    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^readmore/(?P<objectid>\d+)/$',  'readmore', name='readmore'),
    url(r'^search/$',  'search', name='search'),
    url(r'^publish/$',  'publish', name='publish'),
    url(r'^investor_detail/$',  'investor_detail', name='investor_detail'),
    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^checksmscode/$',  'checksmscode', name='checksmscode'),

)

urlpatterns += patterns('searcher.views',
   
    url(r'^send_smscode/$',  'send_smscode', name='send_smscode'),
        )
urlpatterns += patterns('searcher.agreement_views',

    url(r'^write/$',  'writeagreement', name='writeagreement'),
        )
