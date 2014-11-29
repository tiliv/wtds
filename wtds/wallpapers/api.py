from rest_framework import viewsets

from .models import Wallpaper
from .serializers import WallpaperSerializer

class WallpaperViewSet(viewsets.ModelViewSet):
    queryset = Wallpaper.objects.all()
    serializer_class = WallpaperSerializer
