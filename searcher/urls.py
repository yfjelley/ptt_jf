from django.conf.urls import patterns, url

urlpatterns = patterns('searcher.views',
    #url(r'^$', 'index', name='index'),
    url(r'^zc$', 'index_zc', name='index_zc'),
    url(r'^$', 'index_jf', name='index_jf'),
    url(r'^login/$',  'login', name='login'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^register/$',  'register', name='register'),
    url(r'^userinformation/$',  'userinformation', name='userinformation'),
    url(r'getverifycode/$', 'verifycode', name='verifycode'),
    url(r'forgetpw/$', 'forgetpw', name='forgetpw'),



    url(r'^agreement/$',  'agreement', name='agreement'),
    url(r'^guide/$',  'guide', name='guide'),
    url(r'^about/$',  'about', name='about'),
    url(r'^investor/$',  'investor', name='investor'),
    url(r'^contact_us/$',  'contact_us', name='contact_us'),

    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^checksmscode/$',  'checksmscode', name='checksmscode'),

)

urlpatterns += patterns('searcher.views',
   
    url(r'^send_smscode/$',  'send_smscode', name='send_smscode'),
        )
urlpatterns += patterns('searcher.agreement_views',

    url(r'^write/$',  'writeagreement', name='writeagreement'),
        )
