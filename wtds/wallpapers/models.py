from fractions import gcd
import random
from operator import itemgetter
import logging
from decimal import Decimal

from django.db import models
from django.db.models import Avg, F
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager

from wtds.reports import ReportsManager
from .managers import TagManager, WallpaperManager
from .constants import (COMMON_ASPECT_RATIOS, FRIENDLY_ASPECT_RATIOS, RANDOM_STACK_TILT_ANGLES,
        PURITY_CHOICES, MIN_PURITY_RATING, MAX_PURITY_RATING)

logger = logging.getLogger(__name__)

class Tag(TagBase):
    """ Adds a purity rating to the existing taggit ``Tag`` model. """
    purity_rating = models.FloatField(_('purity rating'), default=0, editable=False)

    objects = TagManager()

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('wallpapers:list') + "?tag={}".format(self.slug)
    
    def get_wallpapers(self):
        """ Due to the generic relation between this and ``Wallpaper`` this method eases lookup. """
        return Wallpaper.objects.filter(tags=self)
    
    def get_wallpapers_with_this_tag_only(self):
        """ Returns ``Wallpaper`` objects whose only tag is this one. """
        return Wallpaper.objects.filter_by_orphan_danger(tags=self)

    def get_purity_rating_display(self):
        """ Fakes the normal API for a ``choices`` field. """
        try:
            return PURITY_CHOICES[int(round(self.purity_rating))][1]
        except IndexError:
            rating = self.purity_rating
            self.purity_rating = min(max(self.purity_rating, MIN_PURITY_RATING), MAX_PURITY_RATING)
            logger.error("Tag %r has a purity rating %r outside of the valid range %d-%d."
                    "Normalizing to %d.", self, rating, MIN_PURITY_RATING, MAX_PURITY_RATING,
                    self.purity_rating)
            self.save()

class TaggedWallpaper(GenericTaggedItemBase):
    """ A replacement ``Tag`` model for taggit's API. """
    tag = models.ForeignKey('Tag', related_name="%(app_label)s_%(class)s_items")

class Wallpaper(models.Model):
    objects = WallpaperManager()

    name = models.CharField(_('Name'), max_length=100, blank=True,
            help_text=_("If left blank, the tags will be shown."))
    image = models.ImageField(_('Image'), upload_to='%Y/%m/%d', height_field='height',
            width_field='width')
    height = models.PositiveIntegerField(_('Height'))
    width = models.PositiveIntegerField(_('Width'))
    raw_ratio = models.CharField(max_length=50)
    fractional_ratio = models.DecimalField(max_digits=11, decimal_places=10)
    # color_profile = models.CharField()

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('uploader'),
            help_text=_("Contributing user account"))
    author = models.ForeignKey('Author', verbose_name=_('Author'), blank=True, null=True,
            help_text=_("Original creator"))
    license = models.ForeignKey('License', verbose_name=_('License'), default=8)
    duplicate_of = models.ForeignKey('self', verbose_name=_('Duplicate'), blank=True, null=True)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    is_public = models.BooleanField(_('Public'), default=True)
    purity_rating = models.IntegerField(_('Purity'), choices=PURITY_CHOICES, default=0)

    views = models.PositiveIntegerField(_('Views'), default=0)
    tags = TaggableManager(_('Tags'), blank=False, through=TaggedWallpaper)

    reports = ReportsManager()

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        if self.name:
            return self.name
        return ", ".join(map(str, self.tags.all()))

    def clean(self):
        if self.duplicate_of and self.duplicate_of is self:
            raise ValidationError("Wallpaper can't be marked as a duplicate of itself.")

    def save(self, *args, **kwargs):
        """ Pre-bake the ratio. """
        self.raw_ratio = self.get_aspect_ratio()
        self.fractional_ratio = self.get_fractional_aspect_ratio()
        super(Wallpaper, self).save(*args, **kwargs)

    def assess_tag_purity(self):
        """ Visits each tag and crunches the average purity rating of its wallpapers. """
        return
        # AVG = Avg('wallpapers_taggedwallpaper_items__wallpaper__purity_rating')
        # tags = self.tags.annotate(purity_avg=AVG).exclude(purity_avg=F('purity_rating'))
        # for tag in tags:
        #     logger.info("Tag %r changing purity rating from %r to %r", tag, tag.purity_rating,
        #             tag.purity_avg)
        #     tag.purity_rating = tag.purity_avg
        #     tag.save()

    def get_absolute_url(self):
        return reverse('wallpapers:view', kwargs={'pk': self.pk})

    def get_download_url(self):
        return reverse('wallpapers:download', kwargs={'pk': self.pk})

    def get_full_search_url(self):
        """ Returns the url searching all tags on this wallpaper. """
        tag_slugs = list(self.tags.values_list('slug', flat=True))
        return reverse('wallpapers:list') + "?" + '&'.join('tag='+slug for slug in tag_slugs)

    def get_aspect_ratio(self, as_tuple=False, nearest=True):
        """
        Returns the nearest friendly ratio such as ``16:10``.

        We can find the "nearest" ratio because not all uploads fit perfectly into a standard ratio
        size, but can be set as a wallpaper with simple height cropping.

        """

        divisor = gcd(self.width, self.height)
        rw, rh = (self.width / divisor, self.height / divisor)
        if nearest:
            ratio = sorted(COMMON_ASPECT_RATIOS, key=lambda dim: (rw/rh) / (dim[0]/dim[1]))[-1]
        else:
            ratio = (rw, rh)

        if ratio in FRIENDLY_ASPECT_RATIOS:
            ratio = FRIENDLY_ASPECT_RATIOS[ratio]
        if not as_tuple:
            ratio = ':'.join(map(str, ratio))
        return ratio

    aspect_ratio = property(get_aspect_ratio)

    def get_fractional_aspect_ratio(self):
        ratio = self.get_aspect_ratio()
        x, y = map(Decimal, ratio.split(':'))
        return x / y

    def get_random_stack_tilt(self):
        """ Template UI function that generates a degree rotation value for a "stack". """
        return random.choice(RANDOM_STACK_TILT_ANGLES)

    # Support for wtds.reports app
    @classmethod
    def get_reportable_fields(cls):
        return ('name', 'author', 'license', 'duplicate_of', 'is_public', 'purity_rating', 'tags')

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    name = models.CharField(_('name'), max_length=100, blank=True)
    url = models.URLField(_('url'), max_length=500, blank=True)

    reports = ReportsManager()

    def __str__(self):
        if self.user:
            return str(self.user)
        return self.name or self.url

class License(models.Model):
    name = models.CharField(_('name'), max_length=100)
    short_name = models.CharField(_('short name'), max_length=20)
    summary = models.CharField(_('summary'), max_length=400)

    url = models.URLField(_('url'), max_length=400, blank=True)

    attribute_author = models.BooleanField(_('attribute author'), default=False)
    allow_derivatives = models.BooleanField(_('allow derivatives'), default=False)
    allow_commercial_use = models.BooleanField(_('allow commercial use'), default=False)
    persist_license = models.BooleanField(_('persist license'), default=False)

    def __str__(self):
        return self.name

