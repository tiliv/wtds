import logging

from django.db.models import Manager
from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)

class ProfileManager(Manager):
    def get_query_set(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_active(self, user=None):
        if user:
            if user.is_authenticated():
                return user.profile_set.get_active()
            return self.model()
        return self.get_query_set().get_active()

    def create_default(self, *users):
        """ Creates a default profile for a new user account. """
        profiles = []
        for user in users:
            profiles.append(self.create(user=user, is_active=True))
        if len(users) == 1:
            return profiles[0]
        return dict(zip(users, profiles))

    def deactivate(self):
        return self.get_query_set().deactivate()

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

    def get_query_set(self):
        return FavoriteQuerySet(self.model, using=self._db)

    def filter_through_profile(self, profile):
        return self.get_query_set().filter_through_profile(profile)

    def filter_for_user(self, user):
        return self.get_query_set().filter_for_user(user)

class FavoriteQuerySet(QuerySet):
    def filter_through_profile(self, profile):
        kwargs = FavoriteManager.get_profile_filtering_kwargs(profile)
        return self.filter(**kwargs)

    def filter_for_user(self, user):
        from .models import Profile
        return self.filter_through_profile(Profile.objects.get_active(user))