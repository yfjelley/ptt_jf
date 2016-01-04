from django.conf.urls import patterns, url

urlpatterns = patterns('searcher.views',
    url(r'^zc$', 'index_zc', name='index_zc'),
    url(r'^search_zc$', 'search_zc', name='search_zc'),
    url(r'^auth_register$', 'auth_register', name='auth_register'),
    url(r'^$', 'index_zc', name='index_jf'),
    url(r'^login/$',  'login', name='login'),
    url(r'sendSMS/$','sendSMS',name='sendSMS'),
    url(r'^project_reply/(?P<project_id>\d+)/$', 'project_reply', name='project_reply'),
    url(r'^add_attion/(?P<objectid>\d+)/$',  'add_attion', name='add_attion'),
    url(r'^add_attion_investor/$',  'add_attion_investor', name='add_attion_investor'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^do_search/$',  'do_search', name='do_search'),
    url(r'^do_result/$',  'do_result', name='do_result'),
    url(r'^do_reminder/$',  'do_reminder', name='do_reminder'),
    url(r'^register/$',  'register', name='register'),
    url(r'^userinfo/$',  'userinfo', name='userinfo'),
    url(r'getverifycode/$', 'verifycode', name='verifycode'),
    url(r'forgetpw/$', 'forgetpw', name='forgetpw'),
    url(r'intermediary/(?P<objectid>\d+)/$', 'intermediary', name='intermediary'),
    url(r'^invest_pr/(?P<objectid>\d+)/$',  'invest_pr', name='invest_pr'),

    url(r'^agreement/$',  'agreement', name='agreement'),
    url(r'^safecenter/$',  'safecenter', name='safecenter'),
    url(r'^change_phone_number/$',  'change_phone_number', name='change_phone_number'),
    url(r'^guide/$',  'guide', name='guide'),
    url(r'^about_us/$',  'about_us', name='about_us'),
    url(r'^investor/$',  'investor', name='investor'),
    url(r'^invested/$',  'invested', name='invested'),
    url(r'^search_investor/$',  'search_investor', name='search_investor'),
    url(r'^safety/(?P<objectid>\d+)/$',  'safety', name='safety'),
    url(r'^investor_info/(?P<objectid>\d+)/$',  'investor_info', name='investor_info'),
    url(r'^contact_us/$',  'contact_us', name='contact_us'),
    url(r'^prodetails/(?P<objectid>\d+)/$',  'prodetails', name='prodetails'),

    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^search/$',  'search', name='search'),
    url(r'^search_project/$',  'search_project', name='search_project'),
    url(r'^project/(?P<objectid>\d+)/$',  'project', name='project'),
    url(r'^publish/$',  'publish', name='publish'),
    url(r'^checkuser/$',  'checkuser', name='checkuser'),
    url(r'^checkuser_phone/$',  'checkuser_phone', name='checkuser_phone'),
    url(r'^investor_detail/$',  'investor_detail', name='investor_detail'),
    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^checksmscode/$',  'checksmscode', name='checksmscode'),
    url(r'^uploadify_script/(?P<objectid>\d+)/$', 'uploadify_script'),
    url(r'^delete_uploadfile/$','profile_delte')

)

urlpatterns += patterns('searcher.views',
   
    url(r'^send_smscode/$',  'send_smscode', name='send_smscode'),
    url(r'^send_smscode_modify/$',  'send_smscode_modify', name='send_smscode_modify'),
        )
urlpatterns += patterns('searcher.agreement_views',

    url(r'^write/$',  'writeagreement', name='writeagreement'),
        )
