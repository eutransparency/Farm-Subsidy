import sys
import site
import os

vepath = '/var/www/stage.farmsubsidy.org/lib/python2.6/site-packages'

prev_sys_path = list(sys.path)
# add the site-packages of our virtualenv as a site dir
site.addsitedir(vepath)
# add the app's directory to the PYTHONPATH
sys.path.append('/var/www/stage.farmsubsidy.org/')
sys.path.append('/var/www/stage.farmsubsidy.org/web/')

# reorder sys.path so new directories from the addsitedir show up first
# new_sys_path = [p for p in sys.path if p not in prev_sys_path]
# for item in new_sys_path:
#     sys.path.remove(item)
# sys.path[:0] = new_sys_path

sys.stdout = sys.stderr


# import from down here to pull in possible virtualenv django install
from django.core.handlers.wsgi import WSGIHandler
from web import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# print dir(settings)
# print settings.DATABASE_PORT
os.environ['PYTHON_EGG_CACHE'] = '/var/www/stage.farmsubsidy.org/eggs'


application = WSGIHandler()
