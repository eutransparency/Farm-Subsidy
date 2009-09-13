# encoding: utf-8

import csv
import re
import locale
locale.setlocale(locale.LC_ALL, '')

from farmsubsidy import fsconf
from django.contrib.humanize.templatetags import humanize


def load_info(country=None, format=True, year=fsconf.current_year):
  filepath = "%s/%s/basic_comparisons.csv" % (fsconf.statsdir, year)
  stats = csv.DictReader(open(filepath, "U"))
  if country:
    for row in stats:
      if row['Country'] == country:
        info = row

        
        # delete unwanted elements
        del info['Country']
        # del info['Population']
        # del info['']
        if format:
          # Format elements
          for k,v in info.items():
            try:
              info[k] = humanize.intcomma(info[k])
              formatter = k[-2:]
              if formatter == " E":
                new_k = k[:-2].strip()
                info[new_k] = u"&euro;%s" % info[k]
                del info[k]
              if formatter == "EM":
                new_k = k[:-2].strip()
                info[new_k] = u"&euro;%s Million" % info[k]
                del info[k]
              if formatter == " %":
                new_k = k[:-2].strip()
                info[new_k] = u"%s%%" % info[k]
                del info[k]
                
                
            except Exception,e:
              pass
          # info_sorted = []
          for key, value in info.items():
            del info[key]
            key = re.sub(" ", "_", key.lower())
            key = re.sub("%", "", key)
            info[key] = value
        
  
        return info
  else:
    return stats

def countries_by_category():
  info = load_info()
  cats = {}
  for items in info:
    country = items['Country']
    for cat,value in items.items():
      if cat:
        if cat not in cats:
          cats[cat] = {}
        cats[cat][country] = value
    # break
  del cats['Country']
  # for item in info:
  return cats
  print 
  for cat,data in cats.items():
    print cat, data['GB']
  print 
  # return info









if __name__ == "__main__":
  info = load_info("UK")
  for k,v in info:
    print k,v
