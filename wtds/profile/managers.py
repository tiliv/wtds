from django.db.models import Manager

class ProfileManager(Manager):
    def get_active(self):
        """ Returns the profile marked with ``active=True``. """
        return self.get_query_set().get(is_active=True)