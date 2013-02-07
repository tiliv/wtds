from django.conf.urls import patterns, url, include

from .views import (WallpaperCreateView, WallpaperUpdateView, WallpaperDetailView,
        WallpaperDeleteView, WallpaperListView, TagListView, TagUpdateView, TagDeleteView)

urlpatterns = patterns('',
    url(r'^wallpapers/', include(patterns('',
        url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
        url(r'^list/', include(patterns('',
            url(r'^$', WallpaperListView.as_view(), name='list'),
            url(r'^(?P<slug>[\w-]+)/$', WallpaperListView.as_view(), name='list'),
            url(r'^(?P<ratio>\d+:\d+)/$', WallpaperListView.as_view(), name='list'),
            url(r'^in-danger/all/$', WallpaperListView.as_view(in_danger=True), name='in_danger'),
            url(r'^in-danger/(?P<slug>[\w-]+)/$', WallpaperListView.as_view(in_danger=True), name='in_danger'),
        ))),
        url(r'^(?P<pk>\d+)/', include(patterns('',
            url(r'^$', WallpaperDetailView.as_view(), name='view'),
            url(r'^edit/$', WallpaperUpdateView.as_view(), name='edit'),
            url(r'^delete/$', WallpaperDeleteView.as_view(), name='delete'),
        ))),
    ), namespace='wallpapers')),
    
    url(r'^tags/', include(patterns('',
        url(r'^$', TagListView.as_view(), name='list'),
        url(r'^(?P<slug>[\w-]+)/', include(patterns('',
            url(r'^edit/$', TagUpdateView.as_view(), name='edit'),
            url(r'^delete/$', TagDeleteView.as_view(), name='delete'),
        ))),
    ), namespace='tags')),
)
