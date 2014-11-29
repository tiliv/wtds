from .models import Wallpaper
from .forms import SearchForm

def random_logo_wallpapers(request):
    if not request.user.is_authenticated():
        return {}
    queryset = Wallpaper.objects.filter_through_profile(request.user.active_profile).order_by('?')
    random_queryset = Wallpaper.objects.filter_clean().order_by('?')
    try:
        wallpaper = queryset[0]
    except IndexError:
        # User's profile settings exclude all wallpapers in the database
        try:
            wallpaper = random_queryset[0]
        except IndexError:
            # Welp, we tried. Good luck in development mode, son.
            return {}
    return {
        'logo_wallpaper': wallpaper,
    }

def search_form(request):
    return {
        'search_form': SearchForm(request.GET),
    }
