import datetime
import settings

class Middleware(object):
  def process_response(self, request, response):
    if not request.COOKIES.get('display_welcome_message', False):
      max_age = 15778463
      expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    
      response.set_cookie('display_welcome_message', "0", max_age=max_age, expires=expires)
  
    return response
  