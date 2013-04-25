# Django settings for wtds project.

import os
from os.path import join, abspath, dirname
from django.core.exceptions import ImproperlyConfigured
_dir = lambda *x: join(abspath(dirname(__file__) + "../../.."), *x)
def _var(name):
    """ Get the environment variable or raise exception """
    try:
        return os.environ[name]
    except KeyError:
        error_msg = "Set the %s env variable" % name
        raise ImproperlyConfigured(error_msg)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Tim Valenta', 'tim.valenta@thesimpler.net'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wtds',
        'USER': _var('WTDS_DATABASE_USER'),
        'PASSWORD': _var('WTDS_DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Phoenix'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (_dir('locale'),)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = _dir('..', 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = _dir('..', 'static')
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'auth:login'
LOGOUT_URL = 'auth:logout'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    _dir('wtds', 'core', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = _var('WTDS_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'wtds.profile.middleware.ActiveProfileMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "wtds.core.context_processors.tips",
    "wtds.profile.context_processors.profile_switcher",
    "wtds.wallpapers.context_processors.random_logo_wallpapers",
    "wtds.wallpapers.context_processors.search_form",
)

ROOT_URLCONF = 'wtds.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wtds.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    _dir('wtds', 'core', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.admin',
    # 'django.contrib.admindocs',
    
    # User apps
    'taggit',
    'south',
    'sorl.thumbnail',
    'wtds.core',
    'wtds.reports',
    'wtds.wallpapers',
    'wtds.profile',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(name)s.%(funcName)s:%(lineno)d] %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'thumbnail': {
            'level': 'WARNING',
            'class': 'sorl.thumbnail.log.ThumbnailLogHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'wtds': {
            'handlers': ['mail_admins', 'thumbnail'],
            'level': 'ERROR',
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = 'localhost'
THUMBNAIL_REDIS_PORT = 6379
THUMBNAIL_REDIS_DB = 0
THUMBNAIL_REDIS_PASSWORD = ''
