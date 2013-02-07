from ..models import Wallpaper

def update_ratios(self):
    """ Examines all ``Wallpaper`` objects to set their ``raw_ratio`` fields. """
    for obj in Wallpaper.objects.all():
        obj.height = obj.image.height
        obj.width = obj.image.width
        obj.save() # Triggers ratio generation

