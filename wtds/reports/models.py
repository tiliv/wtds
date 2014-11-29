from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from .managers import ReportManager

class Report(models.Model):
    """ Represents an actionable claim from a visitor concerning a value on the site. """

    objects = ReportManager()

    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    object_fieldname = models.CharField(_('Field'), max_length=50, help_text=_("Specifies the reported field."))
    description = models.CharField(_('Reason'), max_length=500)

    def __str__(self):
        return ':'.join((
            str(self.content_type),
            str(self.content_object),
            self.object_fieldname,
            str(getattr(self.content_object, self.object_fieldname)),
        ))
