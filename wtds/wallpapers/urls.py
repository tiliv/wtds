from django.conf.urls import patterns, url

from .views import WallpaperCreateView

urlpatterns = patterns('',
    url(r'^$', WallpaperCreateView.as_view()),
)
