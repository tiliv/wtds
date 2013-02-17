from .models import Wallpaper
from .forms import SearchForm

def random_logo_wallpapers(request):
    try:
        wallpaper = Wallpaper.objects.filter_for_user(request.user).order_by('?')[0]
    except IndexError:
        # User's profile settings exclude all wallpapers in the database
        wallpaper = Wallpaper.objects.filter_clean().order_by('?')[0]
    return {
        'logo_wallpaper': wallpaper,
    }

def search_form(request):
    return {
        'search_form': SearchForm(request.GET),
    }
