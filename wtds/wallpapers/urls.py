from django.conf.urls import patterns, url

from .views import WallpaperCreateView

urlpatterns = patterns('',
    url(r'^new/$', WallpaperCreateView.as_view(), name='upload'),
)
