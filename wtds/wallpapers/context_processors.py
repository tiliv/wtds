from .models import Wallpaper

def random_logo_wallpapers(request):
    return {
        'logo_wallpaper': Wallpaper.objects.filter_for_user(request.user).order_by('?')[0],
    }
