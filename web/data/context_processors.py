from farmsubsidy.indexer import countryCodes
import urllib
import random

def country(request):
    from django.conf import settings
    countryCode = request.META['PATH_INFO'].split('/')[1]
    
    country = {'code': ''}
    if countryCode in countryCodes.countryCodes():      
      country = {
        'code' : countryCode,
        'name' : countryCodes.code2name[countryCode]
      }
    
    query = request.session.get('query', '')
    
    return {'country': country, 'query' : query}


def message(request):
  pass


def ip_country(request):
  if request.session.get('ip_country',None) == None:
    ip = request.META.get('REMOTE_ADDR') 
    ip_country = urllib.urlopen('http://gaze.mysociety.org/gaze-rest?f=get_country_from_ip&ip=%s' % ip).read()
    if len(ip_country) == 1:
      ip_country = countryCodes.countryCodes()[random.randint(0,22)]
    request.session['ip_country'] = ip_country
    return {'ip_country' : ip_country}
  else:
    # return {'ip_country' : "UK"}
    return {'ip_country' : request.session.get('ip_country',None)}


