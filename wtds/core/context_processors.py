import random
from datetime import datetime

from django.core.cache import cache
from django.conf import settings

TIPS = [
    "Fun fact: if you're using Firefox, you can use the freaking awesome right-click menu features!  Try it by right-clicking a wallpaper tile.",
]

# Patterned after "Sat May 11 20:25:49 2013"
GIT_DATE_FORMAT = "%a %b %d %H:%M:%S %Y"

def tips(request):
    return { 'random_tip': random.choice(TIPS) }

def site_modified_date(request):
    date = cache.get('site_modified_date')
    if date is None:
        try:
            with open(settings.LAST_COMMIT_DATE_FILE) as f:
                date_string = f.read().strip()
        except IOError:
            date = None
        else:
            date = datetime.strptime(date_string, GIT_DATE_FORMAT)
        cache.set('site_modified_date', date, 600)
    return { 'site_modified_date': date }
