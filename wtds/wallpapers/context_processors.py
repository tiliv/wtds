from .models import Wallpaper
from .forms import SearchForm

def random_logo_wallpapers(request):
    queryset = Wallpaper.objects.filter_through_profile(request.user.active_profile).order_by('?')
    try:
        wallpaper = queryset[0]
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
