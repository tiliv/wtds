from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'django.contrib.admin',

    'django_extensions',
    'debug_toolbar',
)

DATABASES['default']['NAME'] = 'wtds2'
