from django.db.models import Manager, Count
from django.db.models.query import QuerySet

class WallpaperManager(Manager):
    def get_query_set(self):
        return WallpaperQuerySet(self.model, using=self._db)

    # Pass through to QuerySet
    def popular(self):
        return self.get_query_set().popular()

    def recent(self):
        return self.get_query_set().recent()

    def filter_by_orphan_danger(self, tags=None):
        return self.get_query_set().filter_by_orphan_danger(tags=tags)

class WallpaperQuerySet(QuerySet):
    def popular(self):
        return self.order_by('id') # FIXME: This isn't a measurement of popularity

    def recent(self):
        return self.order_by('-date_created')

    def filter_by_orphan_danger(self, tags=None):
        """ Filters where the given tags (queryset or an instance) is the wallpaper's only tag. """
        return self.annotate(num_tags=Count('tags')).filter(num_tags=1).filter(tags=tags).distinct()
