from django.conf.urls import patterns, url

from .views import WallpaperCreateView, WallpaperDetailView

urlpatterns = patterns('',
    url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
    url(r'^view/(?P<pk>\d+)/$', WallpaperDetailView.as_view(), name='view'),
)
