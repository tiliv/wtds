import logging

from django.db.models import Manager, Count, Avg, Max
from django.db.models.query import QuerySet

from wtds.profile.models import Profile

logger = logging.getLogger(__name__)

class TagManager(Manager):
    def get_query_set(self):
        return TagQuerySet(self.model, using=self._db)

    def filter_through_profile(self, profile):
        return self.get_query_set().filter_through_profile(profile)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.get_query_set().filter_for_user(user)

class TagQuerySet(QuerySet):
    def filter_through_profile(self, profile):
        terms = {
            'purity_rating__{}'.format(profile.purity_style): profile.purity_rating,
        }
        return self.filter(**terms)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.filter_through_profile(Profile.objects.get_active(user))

class WallpaperManager(Manager):
    def get_query_set(self):
        return WallpaperQuerySet(self.model, using=self._db)

    # Pass through to QuerySet
    def popular(self):
        return self.get_query_set().popular()

    def recent(self):
        return self.get_query_set().recent()

    def filter_by_orphan_danger(self, tags=None):
        return self.get_query_set().filter_by_orphan_danger(tags=tags)

    def filter_through_profile(self, profile):
        return self.get_query_set().filter_through_profile(profile)

    def filter_for_user(self, user):
        """ User might be anonymous, so let the profile manager handle it. """
        return self.filter_through_profile(Profile.objects.get_active(user))

    def filter_clean(self):
        return self.get_query_set().filter_clean()

    def filter_sketchy(self):
        return self.get_query_set().filter_sketchy()

    def filter_nsfw(self):
        return self.get_query_set().filter_nsfw()

    def filter_by_size(self, width, height, variation=0.1):
        return self.get_query_set().filter_similar_by_size(width, height, variation)

    def filter_by_color(self, color_profile):
        return self.get_query_set().filter_similar_by_color(color_profile)

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
        terms = {'purity_rating__{}'.format(profile.purity_style): profile.purity_rating}
        if profile.ratio:
            terms['fractional_ratio__{}'.format(profile.ratio_style)] = profile.get_fractional_ratio()
        if profile.width:
            terms['width__{}'.format(profile.width_style)] = profile.width
        if profile.height:
            terms['height__{}'.format(profile.height_style)] = profile.height
        
        return self.filter(**terms)

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
