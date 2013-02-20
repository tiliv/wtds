from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext as _

from .managers import ReportManager

class Report(models.Model):
    """ Represents an actionable claim from a visitor concerning a value on the site. """

    objects = ReportManager()

    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    object_fieldname = models.CharField(_('field'), max_length=50, help_text=_("Specifies the reported field."))
    description = models.CharField(_('description'), max_length=500)

    def __unicode__(self):
        return ':'.join((
            unicode(self.content_type),
            unicode(self.content_object),
            self.object_fieldname,
            unicode(getattr(self.content_object, self.object_fieldname)),
        ))
