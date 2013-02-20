from django.contrib.contenttypes.generic import GenericRelation

from .models import Report

class ReportsManager(GenericRelation):
    def __init__(self, to=Report, **kwargs):
        super(ReportsManager, self).__init__(to, **kwargs)
