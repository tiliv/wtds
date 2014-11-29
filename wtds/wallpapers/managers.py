import logging

from urllib.parse import urlencode
from functools import reduce

from django.db.models import Manager, Count, Avg, Max
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from wtds.profile.models import Profile

logger = logging.getLogger(__name__)

class TagManager(Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def get_from_request(self, querydict):
        from .forms import SearchForm
        search_form = SearchForm(querydict)
        search_form.full_clean()
        return search_form.cleaned_data['terms']

    # Proxy methods to TagQuerySet
    def filter_through_profile(self, profile):
        return self.get_queryset().filter_through_profile(profile)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.get_queryset().filter_for_user(user)

    def filter_orphaned(self):
        return self.get_queryset().filter_orphaned()

    def annotate_wallpaper_counter(self):
        return self.get_queryset().annotate_wallpaper_counter()

    def get_search_url(self):
        return self.get_queryset().get_search_url()

class TagQuerySet(QuerySet):
    def filter_through_profile(self, profile):
        terms = {
            'purity_rating__{}'.format(profile.purity_style): profile.purity_rating,
        }
        return self.filter(**terms)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.filter_through_profile(Profile.objects.get_active(user))

    def filter_orphaned(self):
        return self.annotate_wallpaper_counter().filter(num_wallpapers=0)

    def annotate_wallpaper_counter(self):
        return self.annotate(num_wallpapers=Count('wallpapers_taggedwallpaper_items__wallpaper'))

    def get_search_url(self):
        """ Returns a URL to a wallpaper search using all of the tags in the queryset. """
        data = [('tag', self.values_list('slug', flat=True))]
        return reverse('wallpapers:list') + "?" + urlencode(data, doseq=True)


class WallpaperManager(Manager):
    @staticmethod
    def get_profile_filtering_kwargs(profile):
        """ Retrieves the filtering kwargs for profile attributes into the Wallpaper attributes. """
        terms = {'purity_rating__{}'.format(profile.purity_style): profile.purity_rating}
        if profile.ratio:
            terms['fractional_ratio__{}'.format(profile.ratio_style)] = profile.get_fractional_ratio()
        if profile.width:
            terms['width__{}'.format(profile.width_style)] = profile.width
        if profile.height:
            terms['height__{}'.format(profile.height_style)] = profile.height
        return terms

    def get_queryset(self):
        return WallpaperQuerySet(self.model, using=self._db)

    # Pass through to QuerySet
    def popular(self):
        return self.get_queryset().popular()

    def recent(self):
        return self.get_queryset().recent()

    def filter_by_orphan_danger(self, tags=None):
        return self.get_queryset().filter_by_orphan_danger(tags=tags)

    def filter_through_profile(self, profile):
        return self.get_queryset().filter_through_profile(profile)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.filter_through_profile(Profile.objects.get_active(user))

    def filter_clean(self):
        return self.get_queryset().filter_clean()

    def filter_sketchy(self):
        return self.get_queryset().filter_sketchy()

    def filter_nsfw(self):
        return self.get_queryset().filter_nsfw()

    def filter_by_size(self, width, height, variation=0.1):
        return self.get_queryset().filter_similar_by_size(width, height, variation)

    def filter_by_color(self, color_profile):
        return self.get_queryset().filter_similar_by_color(color_profile)

    def filter_by_tags(self, tags):
        return self.get_queryset().filter_by_tags(tags)

    def filter_by_tag_names(self, names):
        return self.get_queryset().filter_by_tag_names(names)

    def filter_from_request(self, querydict):
        return self.get_queryset().filter_from_request(querydict)

class WallpaperQuerySet(QuerySet):
    def popular(self):
        return self.order_by('id') # FIXME: This isn't a measurement of popularity

    def recent(self):
        return self.order_by('-date_created')

    def filter_by_orphan_danger(self, tags=None):
        """ Filters where the given tags (queryset or an instance) is the wallpaper's only tag. """
        queryset = self.annotate(num_tags=Count('tags')).filter(num_tags=1)
        if tags:
            queryset = queryset.filter(tags=tags)
        return queryset.distinct()

    def filter_through_profile(self, profile):
        """ Uses options specified by the ``profile`` instance. """
        kwargs = WallpaperManager.get_profile_filtering_kwargs(profile)
        return self.filter(**kwargs)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.filter_through_profile(Profile.objects.get_active(user))

    def filter_clean(self):
        return self.filter(purity_rating=0)

    def filter_sketchy(self):
        return self.filter(purity_rating=1)

    def filter_nsfw(self):
        return self.filter(purity_rating=2)

    def filter_by_size(self, width, height, variation=0.1):
        """ This is primarily a discovery mechanism, so the list is randomized. """
        return self.filter(**{
            'width__gte': width - width * variation,
            'width__lte': width + width * variation,
            'height__gte': height - height * variation,
            'height__lte': height + height * variation,
        }).order_by('?')

    def filter_by_color(self, color_profile):
        # TODO: Implement this
        return self.order_by('?')

    def filter_by_tags(self, tags):
        # Do an AND search on all tags (chaining filters together)
        return reduce(lambda qs, tag: qs.filter(tags=tag), tags, self)

    # def filter_by_tag_slugs(self, slugs):
    #     slugs = filter(bool, slugs)
    #     return reduce(lambda qs, slug: qs.filter(tags__slug=slug), slugs, self)

    def filter_by_tag_names(self, names):
        # Filters out blank values and does a raw search.  Helpful for searching values that aren't actually backed by databased Tag objects.
        names = filter(bool, names)
        return reduce(lambda qs, name: qs.filter(tags__name=name), names, self)

    def filter_from_request(self, querydict):
        return self.filter_by_tag_names(querydict.getlist('tag'))
