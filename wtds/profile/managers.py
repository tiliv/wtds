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

    def get_cleanest(self):
        return self.get_query_set().get_cleanest()

class ProfileQuerySet(QuerySet):
    def get_active(self):
        """ Returns the profile marked with ``active=True``. """
        try:
            return self.get(is_active=True)
        except self.model.DoesNotExist:
            if self.count():
                return self.get_cleanest()
            for field, data in self._known_related_objects.items():
                if field.name == 'user':
                    users = data.values()
                    logger.info("Generating automatic profile for users: %r", users)
                    return self.model.objects.create_default(*users)

    def get_cleanest(self):
        """ Returns the profile with the least risk of showing severe content. """
        return self.order_by('purity_rating')[0]
