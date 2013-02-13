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
            'purity_rating__{}'.format(profile.filter_style): profile.purity_rating,
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
        terms = {
            'purity_rating__{}'.format(profile.filter_style): profile.purity_rating,
        }
        return self.filter(**terms)
