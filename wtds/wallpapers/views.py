from django.views.generic import CreateView

from .models import Wallpaper
from .forms import CreateForm

class WallpaperCreateView(CreateView):
    model = Wallpaper
    
    form_class = CreateForm
