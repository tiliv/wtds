from django.conf.urls import patterns, include, url
from django.conf import settings
# from django.contrib import admin

from .views import HomeView

# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^wallpapers/', include('wtds.wallpapers.urls', namespace='wallpapers')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL.lstrip('/')), 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        })
    )
