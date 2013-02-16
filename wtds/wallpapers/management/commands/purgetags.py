from django.core.management.base import NoArgsCommand
from ...models import Tag

class Command(NoArgsCommand):
    help = "Deletes all orphaned tags, belonging to no wallpapers"

    def handle_noargs(self, **options):
        orphans = Tag.objects.filter_orphaned()
        if orphans:
            self.stdout.write("Found {} orphaned tags.".format(orphans.count()))
            orphans.delete()
            self.stdout.write("Deletion complete.")
        else:
            self.stdout.write("No orphaned tags. No changes to database.")
