from django.template import Library, Node
from farmsubsidy.queries import queries
register = Library()


class LatestLinksNode(Node):
    def __init__(self, bits):
      self.bits = bits
  
    def render(self, context):
      context['recent_links'] = self.bits
      return ''


def get_latest_links(parser, token):
    bits = token.contents.split()
    return LatestLinksNode(bits)

get_latest_links = register.tag(get_latest_links)


def countryBrowse(country, path):
  regions = queries.dumpRegions(country, path)
  # return {'regions' : regions}
  browsepaths = {}
  for region in regions:
    regionpath = "%s/%s" % (path,region)
    if regionpath[0] == "/":
      regionpath = regionpath[1:]
      
    browsepaths[region] = {
      'path' : regionpath,
    }
  return {'regions' : browsepaths, 'country' : country}


register.inclusion_tag('data/blocks/regions.html')(countryBrowse)
