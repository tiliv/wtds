from .models import Wallpaper

def random_logo_wallpapers(request):
    return {
        'logo_wallpaper': Wallpaper.objects.filter_clean().order_by('?')[0],
    }
