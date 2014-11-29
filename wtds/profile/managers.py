import logging

from django.db.models import Manager
from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)

class ProfileManager(Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_active(self, user=None):
        if user:
            if user.is_authenticated():
                return user.profile_set.get_active()
            return self.model()
        return self.get_queryset().get_active()

    def create_default(self, *users):
        """ Creates a default profile for a new user account. """
        profiles = []
        for user in users:
            profiles.append(self.create(user=user, is_active=True))
        if len(users) == 1:
            return profiles[0]
        return dict(zip(users, profiles))

    def deactivate(self):
        return self.get_queryset().deactivate()

class ProfileQuerySet(QuerySet):
    def get_active(self):
        """ Returns the profile marked with ``active=True``. """
        try:
            return self.get(is_active=True)
        except self.model.DoesNotExist:
            if self.count():
                return self.model()
            for field, data in self._known_related_objects.items():
                if field.name == 'user':
                    users = data.values()
                    logger.info("Generating automatic profile for users: %r", users)
                    return self.model.objects.create_default(*users)

    def deactivate(self):
        self.update(is_active=False)

class FavoriteManager(Manager):
    @staticmethod
    def get_profile_filtering_kwargs(profile):
        """
        Prepends all normal Wallpaper filtering kwargs with "wallpaper__" so that they work from
        a Favorite queryset.
        """
        from wtds.wallpapers.managers import WallpaperManager
        kwargs = WallpaperManager.get_profile_filtering_kwargs(profile)
        return {'wallpaper__{}'.format(term): value for term, value in kwargs.items()}

    def get_queryset(self):
        return FavoriteQuerySet(self.model, using=self._db)

    def filter_through_profile(self, profile):
        return self.get_queryset().filter_through_profile(profile)

    def filter_for_user(self, user):
        return self.get_queryset().filter_for_user(user)

    def filter_from_request(self, querydict):
        return self.get_queryset().filter_from_request(querydict)

class FavoriteQuerySet(QuerySet):
    def filter_through_profile(self, profile):
        kwargs = FavoriteManager.get_profile_filtering_kwargs(profile)
        return self.filter(**kwargs)

    def filter_for_user(self, user):
        from .models import Profile
        return self.filter_through_profile(Profile.objects.get_active(user))

    def filter_from_request(self, querydict):
        # FIXME: Because of the way taggit hijacks the query API for its virtual "tags" field, it does incorrect things when it's attribute is not the first part of a relationship-spanning lookup.  For example, "wallpaper__tags__name__in" doesn't work, since taggit rewrites the query as "tagged_item__wallpaper__tags__name__in", which is completely invalid for the Favorite model.  Consequently, this method generates 2 queries instead of 1 direct query.
        from wtds.wallpapers.models import Wallpaper
        tags = querydict.getlist('tag')
        wallpapers = Wallpaper.objects.filter_by_tag_names(tags)
        return self.filter(wallpaper__in=wallpapers)
