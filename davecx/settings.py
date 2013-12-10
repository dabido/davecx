import django.conf.global_settings as DEFAULT_SETTINGS
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dj_database_url
import os

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

APP_REVISION = os.environ.get('APP_REVISION', 'v1')

ADMINS = (
    ('David Mohl', 'dave@dave.cx'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = "davecx"
AWS_QUERYSTRING_AUTH = False

HEROKU_API_KEY = 'xxxx'
HEROKU_APP = 'davecx'

date_after_month = datetime.today() + relativedelta(months=1)
AWS_HEADERS = {
    'Expires': date_after_month.strftime('%a, %d %b %Y %T GMT'),
    'Cache-Control': 'max-age=2419200',
}

DEFAULT_FILE_STORAGE = 'davecx.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'davecx.s3utils.StaticRootS3BotoStorage'

EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', "")
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', "")

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'dave.cx',
    'www.dave.cx',
    'davecx.herokuapp.com'
]

PROJECT_DIR = os.path.dirname(__file__)
MANAGE_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"), # For global static files
    # os.path.abspath(os.path.join(PROJECT_DIR, '..', 'blog/static')) # Blog static files
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"), # For global templates
    os.path.abspath(os.path.join(PROJECT_DIR, '..', 'blog/templates')) # Blog templates
)



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'

STATIC_ROOT = ''
STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dfiamaew_m1t8o*g@v6@1&p6wx=76+9nbmqaz(55ekz3evqc_n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'blog.contextprocessors.provide_data',
)

ROOT_URLCONF = 'davecx.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'davecx.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'blog',
    'heroku-helper'
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
        'TIMEOUT': 500,
        'BINARY': True,
    }
}

try:
    from settings_dev import *
except ImportError: pass