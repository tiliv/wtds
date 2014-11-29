# coding=utf-8

import logging
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from wtds.wallpapers.constants import PURITY_CHOICES
from .managers import ProfileManager, FavoriteManager
from .validators import is_ratio

logger = logging.getLogger(__name__)

FILTER_STYLE_CHOICES = (
    ('exact', 'only'),
    ('lte', 'at most'),
    ('gte', 'at least'),
)
FILTER_STYLE_MATHEMATIC_CHOICES = {
    'exact': '=',
    'lte': '<',
    'gte': '>',
}

class Profile(models.Model):
    """
    Each user may maintain multiple profiles to allow different default settings for searches,
    filters, and purity ratings.
    
    """
    
    objects = ProfileManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    name = models.CharField(_('name'), max_length=100, blank=True)
    is_active = models.BooleanField(_('active'), default=False)

    purity_rating = models.IntegerField(_('purity'), choices=PURITY_CHOICES, default=0)
    purity_style = models.CharField(choices=FILTER_STYLE_CHOICES, max_length=10, default="lte")
    ratio = models.CharField(_('ratio'), validators=[is_ratio], max_length=10, blank=True)
    ratio_style = models.CharField(choices=FILTER_STYLE_CHOICES, max_length=10, default="gte")
    width = models.PositiveIntegerField(_('width'), blank=True, null=True)
    width_style = models.CharField(choices=FILTER_STYLE_CHOICES, max_length=10, default="gte")
    height = models.PositiveIntegerField(_('height'), blank=True, null=True)
    height_style = models.CharField(choices=FILTER_STYLE_CHOICES, max_length=10, default="gte")

    class Meta:
        ordering = ('name', '-id')

    def __str__(self):
        if self.id is None:
            return "[Default]"
        if self.name:
            return self.name
        bits = [self.get_purity_style_display(), self.get_purity_rating_display()]
        if self.ratio:
            bits.append(self.get_ratio_display())
        if self.width or self.height:
            bits.append(u"[{} × {}]".format(self.get_width_display(), self.get_height_display()))
        return " ".join(bits)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.is_active:
            self.user.profile_set.exclude(id=self.id).update(is_active=False)

    def make_active(self):
        self.is_active = True
        self.save()

    def get_fractional_ratio(self):
        """ Returns a floating-point number that is ratio.x / ratio.y """
        if self.ratio:
            x, y = map(Decimal, self.ratio.split(':'))
            return x / y

    def get_ratio_style_mathematic_display(self):
        return FILTER_STYLE_MATHEMATIC_CHOICES[self.ratio_style]

    def get_width_style_mathematic_display(self):
        return FILTER_STYLE_MATHEMATIC_CHOICES[self.width_style]

    def get_height_style_mathematic_display(self):
        return FILTER_STYLE_MATHEMATIC_CHOICES[self.height_style]

    def get_ratio_display(self):
        if self.ratio:
            if self.ratio_style == "exact":
                matching = "@"
            else:
                matching = self.get_ratio_style_mathematic_display()
            return "{}{}".format(matching, self.ratio)
        return "*"

    def get_width_display(self):
        if self.width:
            if self.width_style == "exact":
                return str(self.width)
            else:
                return "{}{}".format(self.get_width_style_mathematic_display(), self.width)
        return "*"

    def get_height_display(self):
        if self.height:
            if self.height_style == "exact":
                return str(self.height)
            else:
                return "{}{}".format(self.get_height_style_mathematic_display(), self.height)
        return "*"

class Favorite(models.Model):

    objects = FavoriteManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    wallpaper = models.ForeignKey('wallpapers.Wallpaper')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
    