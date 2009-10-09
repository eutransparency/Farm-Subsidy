import random
from indexer import countryCodes


def country(request):
    from django.conf import settings
    countryCode = request.META['PATH_INFO'].split('/')[1].upper()
    
    try:
      country = countryCodes.country_codes(countryCode)
    except ValueError:
      country = {'code' : ''}
    
    return {'country': country}


def ip_country(request):

  if request.session.get('ip_country', None) == None:
    try:
      timeout = 3
      socket.setdefaulttimeout(timeout)

      ip = request.META.get('REMOTE_ADDR')
      req = urllib2.Request('http://gaze.mysociety.org/gaze-rest?f=get_country_from_ip&ip=%s' % ip)
      ip_country = urllib2.urlopen(req).read()

      if len(ip_country) == 1:
        raise ValueError

      if ip_country not in countryCodes.country_codes():
        raise ValueError
      
      request.session['ip_country'] = ip_country
      

    except Exception, e:
      ip_country = countryCodes.country_codes()[random.randint(0,22)]
      request.session['ip_country'] = ip_country
  else:
    ip_country = request.session.get('ip_country',None)

  return {'ip_country' : {'ip_country' : ip_country, 'ip_country_name' : countryCodes.country_codes(ip_country)['name']}, }
