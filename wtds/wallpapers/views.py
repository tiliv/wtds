from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from taggit.models import Tag
from taggit.utils import parse_tags

from .models import Wallpaper
from .forms import CreateForm, UpdateForm

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

class WallpaperUpdateView(WallpaperMixin, UpdateView):
    form_class = UpdateForm

class WallpaperDetailView(WallpaperMixin, DetailView):
    pass

class WallpaperDeleteView(WallpaperMixin, DeleteView):
    success_url = reverse_lazy('home')

class WallpaperListView(WallpaperMixin, ListView):
    queryset = Wallpaper.objects.all()
    
    _tags = None

    def get_filter_tags(self):
        if self._tags is None:
            if 'slug' in self.kwargs:
                self._tags = Tag.objects.filter(slug=self.kwargs['slug']) # yields queryset
            else:
                self._tags = Tag.objects.filter(slug__in=self.request.GET.getlist('tag'))
        return self._tags

    # TODO: Sorting
    def get_queryset(self):
        tags = self.get_filter_tags()
        if tags:
            return self.queryset.filter(tags__in=tags).distinct()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(WallpaperListView, self).get_context_data(**kwargs)
        context.update({
            'tags': self.get_filter_tags(),
        })
        return context
        