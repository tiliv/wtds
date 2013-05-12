import random
from datetime import datetime
import logging

from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

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
        except Exception as e:
            logger.error("Problem reading settings.LAST_COMMIT_DATE_FILE %r",
                    settings.LAST_COMMIT_DATE_FILE, exc_info=e)
            date = None
        else:
            date = datetime.strptime(date_string, GIT_DATE_FORMAT)
        cache.set('site_modified_date', date, 600)
    return { 'site_modified_date': date }
