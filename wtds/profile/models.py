from django.db import models
from django.conf import settings

from wtds.wallpapers.constants import PURITY_CHOICES
from .managers import ProfileManager

class Profile(models.Model):
    """
    Each user may maintain multiple profiles to allow different default settings for searches,
    filters, and purity ratings.
    
    """
    
    objects = ProfileManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    is_active = models.BooleanField(default=False)
    purity_rating = models.IntegerField('purity', choices=PURITY_CHOICES, default=0)

    def save(self, *args, **kwargs):
        created = self.id is None

        super(Profile, self).save(*args, **kwargs)
        
        if created:
            profiles = self.profile_set.all()
            if profiles.count() == 0:
                profiles.create_default()
        

