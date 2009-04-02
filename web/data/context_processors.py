from farmsubsidy.indexer import countryCodes

def country(request):
    from django.conf import settings
    countryCode = request.META['PATH_INFO'].split('/')[1]
    country = {'code' : None, 'name' : None}
    if countryCode in countryCodes.countryCodes():      
      country = {
        'code' : countryCode,
        'name' : countryCodes.code2name[countryCode]
      }
    return {'country': country}
