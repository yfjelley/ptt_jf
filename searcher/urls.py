from django.conf.urls import patterns, url

urlpatterns = patterns('searcher.views',
    url(r'^contact/$', 'contact', name='contact'),
    #url(r'^$', 'index', name='index'),
    url(r'^zc$', 'index_zc', name='index_zc'),
    url(r'^$', 'index_jf', name='index_jf'),
    url(r'^login/$',  'login', name='login'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^register/$',  'register', name='register'),
    url(r'^del_reminder/(?P<objectid>\d+)/$',  'del_reminder', name='del_reminder'),
    url(r'^do_reminder/$',  'do_reminder', name='do_reminder'),
    url(r'^userinformation/$',  'userinformation', name='userinformation'),
    url(r'^save_filter/$',  'save_filter', name='save_filter'),
    url(r'getverifycode/$', 'verifycode', name='verifycode'),
    url(r'forgetpw/$', 'forgetpw', name='forgetpw'),
    url(r'modfiypw/$', 'modfiypw', name='modfiypw'),


    url(r'^agreement/$',  'agreement', name='agreement'),
    url(r'^guide/$',  'guide', name='guide'),
    url(r'^about/$',  'about', name='about'),
    url(r'^investor/$',  'investor', name='investor'),
    url(r'^contact_us/$',  'contact_us', name='contact_us'),
    url(r'^disclaimer/$',  'disclaimer', name='disclaimer'),
    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^checksmscode/$',  'checksmscode', name='checksmscode'),
    url(r'^phone_infoPage/$',  'phone_infoPage', name='phone_infoPage'),
)

urlpatterns += patterns('searcher.views',
   
    url(r'^send_smscode/$',  'send_smscode', name='send_smscode'),
        )
urlpatterns += patterns('searcher.agreement_views',

    url(r'^write/$',  'writeagreement', name='writeagreement'),
        )
