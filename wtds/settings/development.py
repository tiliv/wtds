from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'django.contrib.admin',
    'django_extensions',
    'debug_toolbar',
)

# DATABASES['default']['NAME'] = 'wtds2'
LOGGING['formatters']['colored'] = dict(LOGGING['formatters']['default'], **{
    '()': 'djangocolors_formatter.DjangoColorsFormatter',
})
LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'colored',
}
LOGGING['loggers']['wtds'] = {
    'handlers': ['console', 'thumbnail'],
    'level': 'DEBUG',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
