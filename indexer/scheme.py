#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, csv, math
import collections, pprint

def loadScheme(schemefile):
  """Where 'schemefile' is a path to a .scheme file
     Returns a list of field names and key"""
  
  scheme = {}
  
  schemetext = csv.reader(open(schemefile))
  
  # file = open(schemefile,'r')
  # schemetext = file.read() + '\n'
  # file.close()
  fieldMap = fieldNameMappings()
  
  for line in schemetext:
    for key,field in enumerate(line):    
      field = field.lower().strip()
      if field in fieldMap:
        scheme[fieldMap[field]] = key
  return scheme    
  

def fieldNameMappings(): 
  """Returns a dictionary of field names mapped to varible names. The CVS
  files (and the access databases) are very badly inconsistant, in terms of
  field order, field names and field existance (some data isn't availible or
  given).
  
   This is partly the fault of the data given out, but mainly it's a problem
  in the access databases. This function attempts to:
  
   1) Guess what the field is. For example, we might have 'postcode',
  'post_code', 'code_postal', 'zip', 'zip_code' etc etc. The key of the
  dictionary is this value (so, the value in the cvs file, that varies). The
  value is the normalized name, so in the example above 'zipcode' is prefered,
  so fieldMapping['postcode'] = 'zipcode'
  
   2) Store the position in the field order. This comes in handy later when we
  need to figure out what field a particular one is, as there is no standard
  within the schemes.
  """

  fieldMapping = collections.defaultdict(dict)

  fieldMapping['amount'] = 'amount'
  fieldMapping['Amount'] = 'amount'  
  fieldMapping['amount_euro_conversion'] = 'amount'
  fieldMapping['year'] = 'year'
  fieldMapping['Year'] = 'year'  
  fieldMapping['name'] = 'name'
  fieldMapping['geo1'] = 'geo1'
  fieldMapping['geo2'] = 'geo2'  
  fieldMapping['country'] = 'country'

  # Address stuff
  fieldMapping['address'] = 'address1'
  fieldMapping['address1'] = 'address1'
  fieldMapping['address2'] = 'address2'
  fieldMapping['zipcode'] = 'zipcode'
  fieldMapping['geo1'] = 'geo1'
  fieldMapping['geo2'] = 'geo2'
  fieldMapping['geo3'] = 'geo3'
  fieldMapping['geo4'] = 'geo4'

  # Geocode stuff
  fieldMapping['cord_x'] = 'cord_x'
  fieldMapping['cord_y'] = 'cord_y'
  fieldMapping['cord_x'] = 'Lat'
  fieldMapping['cord_y'] = 'Lng'

  #IDs
  fieldMapping['payment_id'] = 'payment_id'
  fieldMapping['recipient_id'] = 'recipient_id'
  fieldMapping['id_recipient_1'] = 'recipient_id'
  fieldMapping['country1_id'] = 'country1_id'
  fieldMapping['country2_id'] = 'country2_id'
  fieldMapping['recipient_id_eu'] = 'recipient_id_eu'
  fieldMapping['recipient_id_x'] = 'recipient_id_x'
  
  # To Add:
    # source
    # country
    # city
    # town
    # zip_area
    # town2
    # Zip_integer
    # notes

  return fieldMapping

  
def fieldTypeMaps(field_value='field_value'):
  """Defines how different fields should be indexed in xapian, including prefixes and values"""
  
  fields = collections.defaultdict(dict)
  
  fields['name'] = {
    'prefix' : 'XNAME',
    'termweight' : 100,
    'index' : True,
    'doc_body' : True,
  }
  
  fields['year'] = {
    'value' : fsconf.index_values['year'],
    'value_formatter': "xapian.sortable_serialise(float(%s))"  % field_value,
    'formatter' : "scheme.calc_year(%s)" % field_value,
    'doc_body' : True,
  }

  fields['amount'] = {
    'value' : fsconf.index_values['amount'],
    'value_formatter': "xapian.sortable_serialise(float(%s))"  % field_value,
    'doc_body' : True,
  }

  fields['country'] = {
    'prefix' : 'XCOUNTRY:',
    'doc_body' : True,
  }

  fields['recipient_id'] = {
    'prefix' : 'XRID:',
    'value' : fsconf.index_values['recipient_id'],
    'value_formatter': "%s"  % field_value,
    'doc_body' : True,
  }

  fields['recipient_id_x'] = {
    'prefix' : 'XRIDX:',
    'value' : fsconf.index_values['recipient_id_x'],
    'value_formatter': "%s"  % field_value,
    'doc_body' : True,
  }


  
  # print eval(fields['year']['formatter'])


  # sys.exit()


  # payment_id
  # geo2
  # country1_id
  # geo1
  # address1
  # address2
  # recipient_id_eu
  # zipcode
  # recipient_id_x


  

  return fields
  
  
  
    
  
def mapSchemeToData(schemefile):
  """Maps a given scheme file to the relivent data file"""
  path = "%s/%s.csv" % (fsconf.csvdir, "/".join(schemefile.split('/')[-3:]).split('.')[0])
  if os.path.exists(path):
    return path
  else:
    raise Exception, "The scheme file %s has no data file mapping at %s" % (schemefile, path)


def calc_year(year,fragile=None):
  """Takes a string in the format of either '2000', '2000-2001' or '2000-2008'
  and does something sane with them"""
  years = str(year).split('-')
  for key,year in enumerate(years):
    years[key] = float(year)

  years_len = len(range(int(years[0]),int(years[-1])))
  if years_len > 2:
    if not fragile:
      return "0"
    else:
      raise ValueError, "Year span too long"
  elif years_len < 1:
    year_int = int(math.ceil(sum(years)))
  else:
    year_int = int(math.ceil(sum(years) / 2))
  return year_int
  
  
if __name__ == '__main__':
  # print loadScheme('/var/www/farmsubsidy/data/scheme/IE/payment/payment.scheme')
 print loadScheme('/Users/sym/Projects/farm-subsidy/data/scheme/AT/payment/austria-20081111--payment20080628.scheme')
