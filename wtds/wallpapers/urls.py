from django.conf.urls import patterns, url, include

from .views import (WallpaperCreateView, WallpaperUpdateView, WallpaperDetailView,
        WallpaperDeleteView, WallpaperListView, TagListView, TagUpdateView, TagDeleteView)

urlpatterns = patterns('',
    url(r'^wallpapers/', include(patterns('',
        # Filtered views
        url(r'^$', WallpaperListView.as_view(), name='list'),
        url(r'^tag/(?P<slug>[\w-]+)/$', WallpaperListView.as_view(), name='list'),
        url(r'^(?P<ratio>\d+:\d+)/$', WallpaperListView.as_view(), name='list'),

        # Special filtered views
        url(r'^in-danger/', include(patterns('',
            url(r'^$', WallpaperListView.as_view(in_danger=True), name='in_danger'),
            url(r'^(?P<slug>[\w-]+)/$', WallpaperListView.as_view(in_danger=True), name='in_danger'),
        ))),

        url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
        url(r'^(?P<pk>\d+)/', include(patterns('',
            url(r'^$', WallpaperDetailView.as_view(), name='view'),
            url(r'^download/$', WallpaperDetailView.as_view(download=True), name='download'),
            url(r'^edit/$', WallpaperUpdateView.as_view(), name='edit'),
            url(r'^delete/$', WallpaperDeleteView.as_view(), name='delete'),
        ))),
    ), namespace='wallpapers')),

    url(r'^tags/', include(patterns('',
        url(r'^$', TagListView.as_view(), name='list'),
        url(r'^inspect/(?P<slug>[\w-]+)/', include(patterns('',
            url(r'^edit/$', TagUpdateView.as_view(), name='edit'),
            url(r'^delete/$', TagDeleteView.as_view(), name='delete'),
        ))),
    ), namespace='tags')),
)
