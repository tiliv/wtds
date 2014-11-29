from django.conf.urls import url, include

from rest_framework import routers

import wtds.wallpapers.api

router = routers.DefaultRouter()
router.register(r'wallpapers', wtds.wallpapers.api.WallpaperViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
