from farmsubsidy.indexer import countryCodes
import socket
import urllib2
import random
import datetime

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
  if request.session.get('ip_country', None) == None:
    try:
      timeout = 3
      socket.setdefaulttimeout(timeout)
      
      ip = request.META.get('REMOTE_ADDR') 
      req = urllib2.Request('http://gaze.mysociety.org/gaze-rest?f=get_country_from_ip&ip=%s' % ip)
      ip_country = urllib2.urlopen(req).read()
      
      if len(ip_country) == 1:
        raise ValueError
      
      # We don't name GB correctly according to ISO. UK is FIPS.
      if ip_country == "GB":
        ip_country = "UK"
      
      request.session['ip_country'] = ip_country
  
      
    except Exception, e:
      ip_country = countryCodes.countryCodes()[random.randint(0,22)]
      request.session['ip_country'] = ip_country
  else:
    ip_country = request.session.get('ip_country',None)

  return {'ip_country' : ip_country }

def welcome_message(request):
  return {'display_welcome_message' : request.COOKIES.get('display_welcome_message', "1")}
  
  
  
  
  
  
  
