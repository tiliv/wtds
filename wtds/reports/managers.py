import logging

from django.db.models import Manager
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

class ReportManager(Manager):
    def get_creation_url(self):
        """ Returns the report creation url for the manager's associated model and instance. """
        model = self.instance.__class__
        return reverse('reports:create', kwargs={
            'contenttype': ContentType.objects.get_for_model(model),
            'model_pk': self.instance.pk,
        })
