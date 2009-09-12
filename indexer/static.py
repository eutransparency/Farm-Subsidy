#!/usr/bin/env python
# encoding: utf-8

from farmsubsidy import fsconf
from farmsubsidy.queries.queries import allterms
import re 

def dumpRegions(country, path=''):
  """dumps all regions in the 'geopath' term in to a file"""
  if path == "":
    path = "XGEOPATH:%s/" % (country.lower())
    offsetnum = 0
  else:
    path = "XGEOPATH:%s/%s" % (country.lower(),re.sub('-', ' ', path).lower())    
    offsetnum = 1
  # return path
  regions = []
  for term in allterms(path):
    region = term.term[len(path):].split('/')[offsetnum]
    if region is not "":
      regions.append(region)
  return set(regions)



if __name__ == "__main__":
  print dumpRegions('uk','england')