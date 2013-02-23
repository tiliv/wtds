from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
# from django.contrib import admin

from .views import HomeView

# admin.autodiscover()

handler403 = 'wtds.core.views.handler403'
handler404 = 'wtds.core.views.handler404'
handler500 = 'wtds.core.views.handler500'

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^', include('wtds.wallpapers.urls')),
    url(r'^account/', include('wtds.profile.urls', namespace="profile")),
    url(r'^reports/', include('wtds.reports.management_urls', namespace="reports")),
    
    # auth
    url(r'^', include(patterns('',
        url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('home')}, name="logout"),
        url(r'^', include('django.contrib.auth.urls')),
    ), namespace='auth')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^~/403/$', handler403, {'fake': True}),
    url(r'^~/404/$', handler404, {'fake': True}),
    url(r'^~/500/$', handler500, {'fake': True}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL.lstrip('/')), 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        })
    )
