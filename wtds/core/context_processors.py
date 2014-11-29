import os.path
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
        path = settings.LAST_COMMIT_DATE_FILE
        if not os.path.isfile(path):
            try:
                with open(path, 'w') as f:
                    f.write('')
            except IOError as e:
                logger.exception("Problem writing empty file %r.", path)
        try:
            with open(path) as f:
                date_string = f.read().strip()
            date = datetime.strptime(date_string, GIT_DATE_FORMAT)
        except IOError as e:
            logger.exception("Problem reading settings.LAST_COMMIT_DATE_FILE %r.", path)
            date = None
        except ValueError as e:
            logger.warning("Can't format date %r.", date_string, exc_info=e)
            date = None
        cache.set('site_modified_date', date, 600)
    return { 'site_modified_date': date }
