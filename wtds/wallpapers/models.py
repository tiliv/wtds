from fractions import gcd
import random

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from .managers import WallpaperManager

FRIENDLY_ASPECT_RATIOS = {
    (8, 5): (16, 10),
}
RANDOM_STACK_TILT_ANGLES = (-4, -3, -2, 2, 3, 4)

class Wallpaper(models.Model):
    objects = WallpaperManager()

    name = models.CharField(max_length=100, blank=True,
            help_text="If left blank, the tags will be shown.")
    image = models.ImageField(upload_to='%Y/%m/%d', height_field='height', width_field='width')
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    # color_profile = models.CharField()

    uploader = models.ForeignKey('auth.User', help_text="Contributing user account")
    author = models.ForeignKey('Author', blank=True, null=True, help_text="Original creator")
    license = models.ForeignKey('License')
    duplicate_of = models.ForeignKey('self', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=False)

    class Meta:
        get_latest_by = 'date_created'

    def __unicode__(self):
        if self.name:
            return self.name
        return u", ".join(map(unicode, self.tags.all()))

    def clean(self):
        if self.duplicate_of and self.duplicate_of is self:
            raise ValidationError("Wallpaper can't be marked as a duplicate of itself.")

    def get_absolute_url(self):
        return reverse('wallpapers:view', kwargs={'pk': self.pk})

    def get_aspect_ratio(self, as_tuple=False):
        """ Returns a friendly ratio such as ``16:10``. """

        divisor = gcd(self.width, self.height)
        ratio = (self.width / divisor, self.height / divisor)
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

    url = models.URLField(max_length=400)

    attribute_author = models.BooleanField()
    allow_derivatives = models.BooleanField()
    allow_commercial_use = models.BooleanField()
    persist_license = models.BooleanField()

    def __unicode__(self):
        return self.name

