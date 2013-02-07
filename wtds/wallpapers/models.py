from fractions import gcd
import random
from operator import itemgetter

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager

from .managers import WallpaperManager
from .constants import (COMMON_ASPECT_RATIOS, FRIENDLY_ASPECT_RATIOS, RANDOM_STACK_TILT_ANGLES,
        PURITY_CHOICES)

class Tag(TagBase):
    """ Adds a purity rating to the existing taggit ``Tag`` model. """
    purity_rating = models.IntegerField(choices=PURITY_CHOICES, default=0)
    
    def get_absolute_url(self):
        return reverse('wallpapers:list', kwargs={'slug': self.slug})
    
    def get_wallpapers(self):
        """ Due to the generic relation between this and ``Wallpaper`` this method eases lookup. """
        return Wallpaper.objects.filter(tags=self)
    
    def get_wallpapers_with_this_tag_only(self):
        """ Returns ``Wallpaper`` objects whose only tag is this one. """
        return Wallpaper.objects.filter_by_orphan_danger(tags=self)

class TaggedWallpaper(GenericTaggedItemBase):
    """ A replacement ``Tag`` model for taggit's API. """
    tag = models.ForeignKey('Tag', related_name="%(app_label)s_%(class)s_items")

class Wallpaper(models.Model):
    objects = WallpaperManager()

    name = models.CharField(max_length=100, blank=True,
            help_text="If left blank, the tags will be shown.")
    image = models.ImageField(upload_to='%Y/%m/%d', height_field='height', width_field='width')
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    raw_ratio = models.CharField(max_length=50)
    # color_profile = models.CharField()

    uploader = models.ForeignKey('auth.User', help_text="Contributing user account")
    author = models.ForeignKey('Author', blank=True, null=True, help_text="Original creator")
    license = models.ForeignKey('License', default=8)
    duplicate_of = models.ForeignKey('self', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    purity_rating = models.IntegerField('purity', choices=PURITY_CHOICES, default=0)

    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=False, through=TaggedWallpaper)

    class Meta:
        get_latest_by = 'date_created'

    def __unicode__(self):
        if self.name:
            return self.name
        return u", ".join(map(unicode, self.tags.all()))

    def clean(self):
        if self.duplicate_of and self.duplicate_of is self:
            raise ValidationError("Wallpaper can't be marked as a duplicate of itself.")

    def save(self, *args, **kwargs):
        """ Pre-bake the ratio. """
        self.raw_ratio = self.get_aspect_ratio()
        super(Wallpaper, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('wallpapers:view', kwargs={'pk': self.pk})

    def get_aspect_ratio(self, as_tuple=False, nearest=True):
        """
        Returns the nearest friendly ratio such as ``16:10``.

        We can find the "nearest" ratio because not all uploads fit perfectly into a standard ratio
        size, but can be set as a wallpaper with simple height cropping.

        """

        divisor = gcd(self.width, self.height)
        rw, rh = (self.width / divisor, self.height / divisor)
        if nearest:
            ratio = sorted(COMMON_ASPECT_RATIOS, key=lambda (w,h): (1.*rw/rh) / (1.*w/h))[-1]
        else:
            ratio = (rw, rh)

        if ratio in FRIENDLY_ASPECT_RATIOS:
            ratio = FRIENDLY_ASPECT_RATIOS[ratio]
        if not as_tuple:
            ratio = ':'.join(map(str, ratio))
        return ratio

    aspect_ratio = property(get_aspect_ratio)

    def get_similar_by_size(self, variation=0.1):
        """ This is primarily a discovery mechanism, so the list is randomized. """

        queryset = Wallpaper.objects.filter(**{
            'width__gte': self.width - self.width * variation,
            'width__lte': self.width + self.width * variation,
            'height__gte': self.height - self.height * variation,
            'height__lte': self.height + self.height * variation,
        })

        return queryset.exclude(pk=self.pk).order_by('?')

    def get_similar_by_color(self):
        # TODO: Implement this
        return Wallpaper.objects.exclude(pk=self.pk).order_by('?')

    def get_random_stack_tilt(self):
        """ Template UI function that generates a degree rotation value for a "stack". """

        return random.choice(RANDOM_STACK_TILT_ANGLES)

    def calculate_purity_rating(self, escalate=True):
        """
        Examines the current tags and their independent purity ratings to compound and independent
        rating for this wallpaper.

        If ``escalate`` is ``True``, then an average rating that is missing in the choices list
        will round up, erring in favor of a more severe rating than a more forgiving one.  If
        ``False``, it will round down.

        """

        ratings = sorted(map(itemgetter(0), PURITY_CHOICES))
        rating = int(self.tags.aggregate(n=models.Avg('purity_rating'))['n'])
        if rating < ratings[0]:
            return ratings[0]
        elif rating > ratings[-1]:
            return ratings[-1]

        slide_factor = 1 if escalate else -1
        while rating not in ratings:
            rating += slide_factor
        return rating

class Author(models.Model):
    user = models.OneToOneField('auth.User', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    url = models.URLField(max_length=500, blank=True)

    # class Meta:
    #     unique_together = ('name', 'url')
    #
    def __unicode__(self):
        return (self.user.get_full_name() if self.user else self.name) or self.url

class License(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    summary = models.CharField(max_length=400)

    url = models.URLField(max_length=400, blank=True)

    attribute_author = models.BooleanField()
    allow_derivatives = models.BooleanField()
    allow_commercial_use = models.BooleanField()
    persist_license = models.BooleanField()

    def __unicode__(self):
        return self.name

