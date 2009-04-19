from django.template import Library, Node
import urllib
import math

register = Library()

def format_url(results,page=0):
  get = dict(results['GET'])
  if page > 0:
    get['page'] = page
  elif 'page' in get:
    del get['page']
  url = urllib.urlencode(get, True)

  active = False
  if results['pager']['page'] == page:
    active = True
  
  return {'url' : "?%s" % url, 'active' : active}

def pager(results):
  
  total_pages = int(math.ceil(results['pager']['results'] / results['pager']['len']))
  current_page = results['pager']['page']
  
  if current_page != total_pages:
    next_page = format_url(results,current_page+1)
  
  if current_page != 0:
    previous_page = format_url(results,current_page-1)
  
  i=0
  pages_left = []
  while i<5 and i<total_pages:
    pages_left.append((format_url(results,i),i+1))
    i += 1
    
  i=total_pages
  pages_right = []
  while i>5 and i>len(pages_left) and i>total_pages-5:
    pages_right.append((format_url(results,i),i+1))
    i -= 1
  pages_right.reverse()  
  
  if current_page >= 3:
    if current_page <= 5:
      i = 5
      pages_to = current_page+8
    elif current_page-3 <= 5:
      i=5
      pages_to=11
    elif current_page+4 >= total_pages-4:
      i=current_page-10
      pages_to=total_pages-4
    else:
      i=current_page-2
      pages_to = current_page+5
    pages_centre = []
    while i<pages_to:
      pages_centre.append((format_url(results,i),i+1))
      i += 1
  
    if total_pages > 1:
      last_page = format_url(results,total_pages)
      first_page = format_url(results,0)
  
  
  
  return locals()

register.inclusion_tag('blocks/pager.html')(pager)

