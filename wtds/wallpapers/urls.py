from django.conf.urls import patterns, url, include

from .views import WallpaperCreateView, WallpaperDetailView, WallpaperDeleteView

urlpatterns = patterns('',
    url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
    url(r'^(?P<pk>\d+)/', include(patterns('',
        url(r'^$', WallpaperDetailView.as_view(), name='view'),
        url(r'^delete/$', WallpaperDeleteView.as_view(), name='delete'),
    ))),
)
