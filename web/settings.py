# Django settings for farmjango project.

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'farmjango'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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
MEDIA_ROOT = '/var/www/farmsubsidy/web/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'media'

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
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',    
    'pagination.middleware.PaginationMiddleware',
    'misc.middleware.Middleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    
)

ROOT_URLCONF = 'web.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/www/farmsubsidy/web/templates',
    '/var/www/farmsubsidy/web/groups/templates',
)


INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.syndication',
    'farmsubsidy.web.api',
    'farmsubsidy.web.comments',
    'farmsubsidy.web.countryinfo',
    'farmsubsidy.web.customlists',
    'farmsubsidy.web.data',
    'farmsubsidy.web.feeds',
    'farmsubsidy.web.graphs',
    'farmsubsidy.web.misc',
    'pagination',
    'registration',
    'profiles',
)


TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  'data.context_processors.country',
  'data.context_processors.ip_country',
  'data.context_processors.welcome_message',
  'customlists.context_processors.list_items',
  'misc.context_processors.latest_tweet',
)



ACCOUNT_ACTIVATION_DAYS = 7
# LOGIN_REDIRECT_URL = "/user/profile"
AUTH_PROFILE_MODULE = "misc.Profile"
DEFAULT_FROM_EMAIL = "team@farmsubsidy.org"


CACHE_BACKEND = 'file:///var/tmp/django_cache'


TWITTER_USER = "farmsubsidy"
TWITTER_TIMEOUT = 3600
