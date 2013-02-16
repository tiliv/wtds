import os.path
import mimetypes

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.db.models import Count

from taggit.utils import parse_tags

from .models import Wallpaper, Tag
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
        self.object.assess_tag_purity()

        return HttpResponseRedirect(self.get_success_url())

class WallpaperUpdateView(AuthenticationMixin, WallpaperMixin, UpdateView):
    permissions_required = ['wallpapers.change_wallpaper']
    form_class = UpdateForm

    def form_valid(self, form):
        response = super(WallpaperUpdateView, self).form_valid(form)
        self.object.assess_tag_purity()
        return response

class WallpaperDetailView(WallpaperMixin, DetailView):
    download = False

    def get(self, request, *args, **kwargs):
        if self.download:
            return self.download_content(request, *args, **kwargs)
        return super(WallpaperDetailView, self).get(request, *args, **kwargs)

    def download_content(self, request, *args, **kwargs):
        """ Works like the ``get`` or ``post`` methods. Returns an HttpResponse. """
        wallpaper = self.get_object()
        filename = os.path.basename(wallpaper.image.name)
        content_type = mimetypes.guess_type(filename)[0]

        response = StreamingHttpResponse(wallpaper.image, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response

    def get_context_data(self, **kwargs):
        context = super(WallpaperDetailView, self).get_context_data(**kwargs)
        user_wallpapers = Wallpaper.objects.filter_for_user(self.request.user) \
                .exclude(pk=self.object.pk)
        context.update({
            'similar': {
                'tags': self.object.tags.similar_objects()[:2],
                'size': user_wallpapers.filter_by_size(self.object.width, self.object.height)[:2],
                'color': user_wallpapers.filter_by_color(None)[:2] # FIXME: Implement color profile
            }
        })
        return context
        

class WallpaperDeleteView(AuthenticationMixin, WallpaperMixin, DeleteView):
    permissions_required = ['wallpapers.delete_wallpaper']
    success_url = reverse_lazy('home')

class WallpaperListView(WallpaperMixin, ListView):
    _tags = None

    # If set, a single-tag filter will only show results that have that tag as their only tag.
    in_danger = False

    def get_filter_tags(self):
        if self._tags is None:
            if 'slug' in self.kwargs:
                self._tags = Tag.objects.filter(slug=self.kwargs['slug']) # yields queryset
            else:
                self._tags = Tag.objects.filter(slug__in=self.request.GET.getlist('tag'))
        return self._tags

    # TODO: Sorting
    def get_queryset(self):
        queryset = Wallpaper.objects.filter_for_user(self.request.user)
        if 'ratio' in self.kwargs:
            queryset = queryset.filter()
        else:
            tags = self.get_filter_tags()
            if self.in_danger:
                queryset = Wallpaper.objects.filter_by_orphan_danger(tags=tags)
            else:
                if tags:
                    queryset = queryset.filter(tags__in=tags).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WallpaperListView, self).get_context_data(**kwargs)
        context.update({
            'tags': self.get_filter_tags(),
            'in_danger': self.in_danger,
        })
        return context


class TagMixin(object):
    model = Tag

class TagListView(TagMixin, ListView):
    queryset = Tag.objects.annotate_wallpaper_counter().order_by('purity_rating', 'name')

    profile_filtering = True

    def get_queryset(self):
        queryset = self.queryset
        if self.profile_filtering:
            queryset = queryset.filter_for_user(self.request.user)
        return queryset

class TagOrphanedListView(AuthenticationMixin, TagListView):
    permissions_required = ['wallpaper.delete_tag']

    orphaned = True # Flag for template rendering

    def get_queryset(self):
        queryset = super(TagOrphanedListView, self).get_queryset()
        return queryset.filter(num_wallpapers=0)

class TagUpdateView(AuthenticationMixin, TagMixin, UpdateView):
    permissions_required = ['wallpapers.change_tag']
    form_class = modelform_factory(Tag, fields=('name',))

class TagDeleteView(AuthenticationMixin, TagMixin, DeleteView):
    permissions_required = ['wallpapers.delete_tag']
    success_url = reverse_lazy('tags:list')

    def post(self, request, *args, **kwargs):
        if self.get_object().get_wallpapers_with_this_tag_only().count():
            return HttpResponseForbidden()
        return super(TagDeleteView, self).post(request, *args, **kwargs)
