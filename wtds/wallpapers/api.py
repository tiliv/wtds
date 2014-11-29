from rest_framework import viewsets

from .models import Wallpaper

class WallpaperViewSet(viewsets.ModelViewSet):
    queryset = Wallpaper.objects.all()
    model = Wallpaper
