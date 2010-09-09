# Django settings for farmjango project.
import os 
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.split(PROJECT_PATH)[0]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH + '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dm195c_n(qv4!x-o7!5akh$q19vvrw$o6@2p_&^e(()qi6zojl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django_notify.middleware.NotificationsMiddleware',    
    'web.misc.middleware.Middleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    
)

ROOT_URLCONF = 'web.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.syndication',
    'django_notify',
    'web.api',
    'web.comments',
    'web.countryinfo',
    'data',
    'search',
    'feeds',
    'graphs',
    'misc',
    'pagination',
    'tagging',
    'registration',
    'profiles',
    'devserver',   
    'treebeard',
    'haystack',
    'listmaker',
    'features',
    'django.contrib.gis',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  'data.context_processors.country',
  'data.context_processors.ip_country',
  'listmaker.context_processors.list_items',
  # 'misc.context_processors.latest_tweet',
  'misc.context_processors.google_api_key',
  'misc.context_processors.header_class',  
  'data.context_processors.breadcrumb',
  'features.context_processors.featured_items',
)

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = '/login/'
AUTH_PROFILE_MODULE = "misc.Profile"
DEFAULT_FROM_EMAIL = "team@farmsubsidy.org"


TWITTER_USER = "farmsubsidy"
TWITTER_TIMEOUT = 3600

DEFAULT_CHARSET = "utf8" 

INTERNAL_IPS = ('127.0.0.1',)

COMMENTS_APP = 'web.comments'

EMAIL_PORT = 1025

HAYSTACK_SITECONF = 'search_conf'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = ROOT_PATH + '/xapian.db'
HAYSTACK_BATCH_SIZE = 100000
HAYSTACK_INCLUDE_SPELLING = True

DEFAULT_YEAR = 0
STATS_YEAR = 2008
STATS_DIR = ROOT_PATH + '/data/stats'

PISTON_DISPLAY_ERRORS = False

TEST_RUNNER='django.contrib.gis.tests.run_tests'
POSTGIS_TEMPLATE='template_postgis'