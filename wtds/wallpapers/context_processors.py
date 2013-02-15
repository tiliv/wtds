from .models import Wallpaper

def random_logo_wallpapers(request):
    try:
        wallpaper = Wallpaper.objects.filter_for_user(request.user).order_by('?')[0]
    except IndexError:
        # User's profile settings exclude all wallpapers in the database
        wallpaper = Wallpaper.objects.filter_clean().order_by('?')[0]
    return {
        'logo_wallpaper': wallpaper,
    }
