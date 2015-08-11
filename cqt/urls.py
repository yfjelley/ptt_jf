from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'cqt.views.home', name='home'),
    url(r'^account/$', 'cqt.views.account', name='register'),
)
