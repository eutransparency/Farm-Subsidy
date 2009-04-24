from django.template import Library, Node
from django.core.urlresolvers import reverse
import urllib

register = Library()

def recipient_links(recipient):
  recipient_name = recipient
  recipient_url = urllib.urlencode({'x' : recipient})[2:]
  links = (
    ("Blogs mentioning '%s'" % recipient_name, "http://blogsearch.google.com/blogsearch?q=%s" % recipient_url),
    ("Search google for '%s'"  % recipient_name, "http://www.google.co.uk/search?q=%s" % recipient_url),
    ("Search Wikipedia for '%s'"  % recipient_name, "http://en.wikipedia.org/w/index.php?title=Special%%3ASearch&search=%s&fulltext=Search" % recipient_url),
    ("'%s' on Google Finance" % recipient_name, "http://www.google.com/finance?q=%s" % recipient_url),
  )
  return {"links" : links}
  
register.inclusion_tag('blocks/recipient_links.html')(recipient_links)


def link_to_recipient(recipient):
  recipient_name = recipient['name']
  recipient_url = "%s%s/%s" % (
    "http://www.farmsubsidy.org",
    reverse('recipient_view', kwargs={'recipient_id' : recipient['recipient_id_x'], 'country' : recipient['country']}),
    recipient['name']
    )
    
  links = (
    ('your blog', '<a href="%s">%s</a>' % (recipient_url, recipient_name)),
    ('wikipedia', '[%s] (%s)' % (recipient_url, recipient_name)),
  )
  return {"links" : links}
register.inclusion_tag('blocks/link_to_recipient.html')(link_to_recipient)