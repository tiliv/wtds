from django.conf.urls import patterns, url, include

from .views import WallpaperCreateView, WallpaperDetailView, WallpaperDeleteView, WallpaperListView

urlpatterns = patterns('',
    url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
    url(r'^list/', include(patterns('',
        url(r'^$', WallpaperListView.as_view(), name='list'),
        url(r'^(?P<slug>[\w-]+)/$', WallpaperListView.as_view(), name='list'),
    ))),
    url(r'^(?P<pk>\d+)/', include(patterns('',
        url(r'^$', WallpaperDetailView.as_view(), name='view'),
        url(r'^delete/$', WallpaperDeleteView.as_view(), name='delete'),
    ))),
)
