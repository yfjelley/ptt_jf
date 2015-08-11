from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from bbs import forum
import bbs
from ddbid import settings


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ddbid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bbs/', include('bbs.forum.urls')),
    url(r'^user/', include('bbs.account.urls')),
    url(r'^', include('searcher.urls')),
    url(r'^api/forum/', include(bbs.forum.urls.api_urlpatterns)),
    url(r'^panel/', include('bbs.panel.urls', namespace='panel', app_name='panel')),
    url(r'^emoji/', include('emoji.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
