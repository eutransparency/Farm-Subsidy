from farmsubsidy.indexer import countryCodes

def country(request):
    from django.conf import settings
    countryCode = request.META['PATH_INFO'].split('/')[1]

    if countryCode in countryCodes.countryCodes():      
      country = {
        'code' : countryCode,
        'name' : countryCodes.code2name[countryCode]
      }
    country = {'code' : 'UK', 'name' : 'United Kingdom'}
    return {'country': country}
