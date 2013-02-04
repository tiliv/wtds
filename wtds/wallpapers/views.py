from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect

from .models import Wallpaper
from .forms import CreateForm

class WallpaperMixin(object):
    model = Wallpaper

class WallpaperCreateView(WallpaperMixin, CreateView):
    form_class = CreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploader = self.request.user
        self.object.save()

        # Saves the tags
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())

class WallpaperDetailView(WallpaperMixin, DetailView):
    pass
