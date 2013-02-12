import logging

from django.db import models
from django.conf import settings

from wtds.wallpapers.constants import PURITY_CHOICES
from .managers import ProfileManager

logger = logging.getLogger(__name__)

class Profile(models.Model):
    """
    Each user may maintain multiple profiles to allow different default settings for searches,
    filters, and purity ratings.
    
    """
    
    objects = ProfileManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    purity_rating = models.IntegerField('purity', choices=PURITY_CHOICES, default=0)

    class Meta:
        ordering = ('name', '-id')

    def __unicode__(self):
        return self.name or self.get_purity_rating_display()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.is_active:
            self.user.profile_set.exclude(id=self.id).update(is_active=False)

    def make_active(self):
        self.is_active = True
        self.save()
