from django.conf.urls import patterns, url

urlpatterns = patterns('searcher.views',
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^$', 'index', name='index'),
    url(r'^login/$',  'login', name='login'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^register/$',  'register', name='register'),
    url(r'^add_favoritebid/(?P<objectid>\d+)/$',  'add_favoritebid', name='add_favoritebid'),
    url(r'^add_favoriteplatform/(?P<objectid>\d+)/$',  'add_favoriteplatform', name='add_favoriteplatform'),
    url(r'^add_reminder/(?P<objectid>\d+)/$',  'add_reminder', name='add_reminder'),
    url(r'^del_reminder/(?P<objectid>\d+)/$',  'del_reminder', name='del_reminder'),
    url(r'^do_reminder/$',  'do_reminder', name='do_reminder'),
    url(r'^myfavorite/(?P<tid>\d+)/$$',  'myfavorite', name='myfavorite'),
    url(r'^platform/$',  'platform', name='platform'),
    url(r'^userinformation/$',  'userinformation', name='userinformation'),
    url(r'^save_filter/$',  'save_filter', name='save_filter'),
    url(r'^del_filter/(?P<fid>\d+)/$',  'del_filter', name='del_filter'),
    url(r'^bid_detail/(?P<objectid>\d+)/$',  'bid_detail', name='bid_detail'),
    url(r'^comb_detail/(?P<ids>[^/]+)/$',  'comb_detail', name='comb_detail'),
    url(r'^shortcut_request/(?P<objectid>\d+)/$',  'shortcut_request', name='shortcut_request'),
    url(r'getverifycode/$', 'verifycode', name='verifycode'),
    url(r'forgetpw/$', 'forgetpw', name='forgetpw'),
    url(r'modfiypw/$', 'modfiypw', name='modfiypw'),

    # url(r'^other_page_reg/$',  'other_page_reg', name='other_page_reg'),
    # url(r'^other_reg/$',  'other_reg', name='other_reg'),
    url(r'^about_us/$',  'about_us', name='about_us'),
    url(r'^contact_us/$',  'contact_us', name='contact_us'),
    url(r'^disclaimer/$',  'disclaimer', name='disclaimer'),
    url(r'^checkvcode/$',  'checkvcode', name='checkvcode'),
    url(r'^checksmscode/$',  'checksmscode', name='checksmscode'),
    url(r'^phone_infoPage/$',  'phone_infoPage', name='phone_infoPage'),
)

urlpatterns += patterns('searcher.viewss',
    url(r'^qq_is_first/$',  'qq_is_first', name='qq_is_first'),
    url(r'^wb_is_first/$',  'wb_is_first', name='wb_is_first'),
    url(r'^ch_access_token/$',  'ch_access_token', name='ch_access_token'),
    url(r'^test_thread/$',  'remind_thread', name='remind_thread'),
    url(r'^test_thread_on/$',  'test_thread_on', name='test_thread_on'),
    url(r'^send_message/$',  'send_message', name='send_message'),
)


urlpatterns += patterns('searcher.views',
   
    url(r'^send_smscode/$',  'send_smscode', name='send_smscode'),
        )
