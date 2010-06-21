import os, sys
import site

prev_sys_path = list(sys.path)

sys.path.append('/var/www/stage.farmsubsidy.org/')
sys.path.append('/var/www/stage.farmsubsidy.org/web')
vepath = '/var/www/stage.farmsubsidy.org/lib/python2.6/site-packages'
site.addsitedir(vepath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path

import sys
for p in sys.path:
  print >> sys.stderr, "*********************************%s" % p


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

