import os.path
import mimetypes
import json
import logging

from django.views.generic import View, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.http import (StreamingHttpResponse, HttpResponse, HttpResponseRedirect,
        HttpResponseForbidden)
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.db.models import Count

from taggit.utils import parse_tags

from wtds.core.views import AuthenticationMixin
from .models import Wallpaper, Tag
from .forms import CreateForm, UpdateForm, SearchForm

logger = logging.getLogger(__name__)

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
        similar_via_tags = self.object.tags.similar_objects()
        user_wallpapers = Wallpaper.objects.filter_for_user(self.request.user) \
                .exclude(pk=self.object.pk)
        context.update({
            'similar': {
                'tags': similar_via_tags[:2],
                'size': user_wallpapers.filter_by_size(self.object.width, self.object.height)[:2],
                'color': user_wallpapers.filter_by_color(None)[:2] # FIXME: Implement color profile
            }
        })
        return context
        

class WallpaperDeleteView(AuthenticationMixin, WallpaperMixin, DeleteView):
    permissions_required = ['wallpapers.delete_wallpaper']
    success_url = reverse_lazy('home')

class WallpaperListView(WallpaperMixin, ListView):
    # If set, a single-tag filter will only show results that have that tag as their only tag.
    in_danger = False

    def get_filter_tags(self):
        search_form = SearchForm(self.request.GET)
        search_form.full_clean()
        return search_form.cleaned_data['terms']

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
                # Do an AND search on all tags (chaining filters together)
                queryset = reduce(lambda qs, tag: qs.filter(tags=tag), tags, queryset)
        return queryset.distinct()

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

class TagAutocompleteView(TagMixin, View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', "").strip()
        tags = Tag.objects.filter_for_user(self.request.user)
        choices = list(tags.filter(name__istartswith=term).values_list('name', 'slug'))
        choices = map(lambda (name, slug): {'label': name, 'value': slug}, choices)
        return HttpResponse(json.dumps(choices), content_type="text/json")
