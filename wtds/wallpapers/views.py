import os.path
import mimetypes
import json
import logging
from operator import attrgetter

from django.views.generic import View, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.http import (StreamingHttpResponse, HttpResponse, HttpResponseRedirect,
        HttpResponseForbidden)
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.db.models import Count

from taggit.utils import parse_tags

from wtds.core.views import AuthenticationMixin
from .models import Wallpaper, Tag
from .forms import CreateForm, UpdateForm
from .decorators import requires_authorship

logger = logging.getLogger(__name__)

class WallpaperMixin(object):
    model = Wallpaper

    def get_queryset(self):
        return self.model.objects.filter(is_public=True)

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

    @requires_authorship
    def dispatch(self, request, *args, **kwargs):
        """ Adds extra verification that the wallpaper is owned by the user. """
        return super(WallpaperUpdateView, self).dispatch(request, *args, **kwargs)

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

    def get_queryset(self):
        queryset = super(WallpaperDetailView, self).get_queryset()
        return queryset.annotate(is_favorite=Count('favorite'))

    def get_context_data(self, **kwargs):
        context = super(WallpaperDetailView, self).get_context_data(**kwargs)
        similar_via_tags = self.object.tags.similar_objects()
        user_wallpapers = Wallpaper.objects.filter_for_user(self.request.user) \
                .exclude(pk=self.object.pk)
        context.update({
            'similar': {
                'tags': user_wallpapers.filter(id__in=tuple(map(attrgetter('id'), similar_via_tags))[:2]),
                'size': user_wallpapers.filter_by_size(self.object.width, self.object.height)[:2],
                'color': user_wallpapers.filter_by_color(None)[:2] # FIXME: Implement color profile
            },
        })
        return context
        

class WallpaperDeleteView(AuthenticationMixin, WallpaperMixin, DeleteView):
    permissions_required = ['wallpapers.delete_wallpaper']
    success_url = reverse_lazy('home')

class WallpaperListView(WallpaperMixin, ListView):
    # If set, a single-tag filter will only show results that have that tag as their only tag.
    in_danger = False

    # TODO: Sorting
    def get_queryset(self):
        queryset = Wallpaper.objects.filter_for_user(self.request.user)
        self._tags = None
        if 'ratio' in self.kwargs:
            queryset = queryset.filter()
        else:
            self._tags = Tag.objects.get_from_request(self.request.GET)
            if self.in_danger:
                queryset = Wallpaper.objects.filter_by_orphan_danger(tags=self._tags)
            else:
                queryset = queryset.filter_by_tags(self._tags)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(WallpaperListView, self).get_context_data(**kwargs)
        context.update({
            'tags': self._tags,
            'in_danger': self.in_danger,
        })
        return context


class TagMixin(object):
    model = Tag

class TagListView(TagMixin, ListView):
    profile_filtering = True

    def get_queryset(self):
        queryset = Tag.objects.annotate_wallpaper_counter().order_by('purity_rating', 'name')
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

class TagAutocompleteView(TagMixin, View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', "").strip()
        tags = Tag.objects.filter_for_user(self.request.user)
        choices = list(tags.filter(name__istartswith=term).values_list('name', flat=True))
        return HttpResponse(json.dumps(choices), content_type="text/json")
