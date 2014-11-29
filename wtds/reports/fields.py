from django.contrib.contenttypes.generic import GenericRelation

# from south.modelsinspector import add_introspection_rules

from .models import Report

class ReportsManager(GenericRelation):
    def __init__(self, to=Report, **kwargs):
        super(ReportsManager, self).__init__(to, **kwargs)

# rules = [
#     ([ReportsManager], [], {
#         'to': ["rel.to", {"default": Report}],
#     }),
# ]
# add_introspection_rules(rules, [r"^wtds\.reports\.fields\.ReportsManager"])
