from django.db import models
from django.conf import settings

from wtds.wallpapers.constants import PURITY_CHOICES

class Profile(models.Model):
    """
    Each user may maintain multiple profiles to allow different default settings for searches,
    filters, and purity ratings.
    
    """
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    purity_rating = models.IntegerField('purity', choices=PURITY_CHOICES, default=0)

