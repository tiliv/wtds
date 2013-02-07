from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from taggit.models import Tag
from taggit.utils import parse_tags

from .models import Wallpaper
from .forms import CreateForm, UpdateForm

class AuthenticationMixin(object):
    login_required = True
    permissions_required = []
    
    def dispatch(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('auth:login'))
        if self.permissions_required:
            for permission in self.permissions_required:
                if not self.request.user.has_perm(permission):
                    return HttpResponseForbidden("Sorry! You don't have permission to go there.")
        return super(AuthenticationMixin, self).dispatch(request, *args, **kwargs)
    

class WallpaperMixin(object):
    model = Wallpaper

class WallpaperCreateView(AuthenticationMixin, WallpaperMixin, CreateView):
    permissions_required = ['wallpapers.add_wallpaper']
    form_class = CreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploader = self.request.user
        self.object.save()

        # Saves the tags
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())

class WallpaperUpdateView(AuthenticationMixin, WallpaperMixin, UpdateView):
    permissions_required = ['wallpapers.change_wallpaper']
    form_class = UpdateForm

class WallpaperDetailView(WallpaperMixin, DetailView):
    pass

class WallpaperDeleteView(AuthenticationMixin, WallpaperMixin, DeleteView):
    permissions_required = ['wallpapers.delete_wallpaper']
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
        queryset = self.queryset
        if 'ratio' in self.kwargs:
            queryset = queryset.filter()
        else:
            tags = self.get_filter_tags()
            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WallpaperListView, self).get_context_data(**kwargs)
        context.update({
            'tags': self.get_filter_tags(),
        })
        return context
