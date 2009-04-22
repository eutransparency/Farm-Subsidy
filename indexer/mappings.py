#!/usr/bin/env python
# encoding: utf-8
"""
mappings.py
"""

from farmsubsidy import fsconf
import collections


def fieldTypeMaps(field_value='field_value'):
  """Defines how different fields should be 
  indexed and queried by xapian, including prefixes and values
  
  This function is used by both the indexer and the qurey parser
  to add proper prefixed to the search.  
  
  For indexing, if a field needs formatting before being indexed 
  (see 'year') then use 'formatter' to call a function though eval()
  
  - 'field_value' is the name of the field varible passed to the function
    and is used at index time.  See indexer.index_line() for more.
  
  """
  
  fields = collections.defaultdict(dict)

  fields['global_id'] = {
    'prefix' : 'GID:',
    'name' : 'gid',
    'doc_body' : True,
  }

  fields['global_id_x'] = {
    'prefix' : 'GIDX:',
    'name' : 'gidx',
    'value' : fsconf.index_values['global_id_x'],
    'value_formatter': "%s"  % field_value,    
    'doc_body' : True,
  }

  
  fields['name'] = {
    'prefix' : 'XNAME:',
    'name' : 'name',
    'termweight' : 1000,
    'index' : True,
    'doc_body' : True,
  }
  
  fields['year'] = {
    'value' : fsconf.index_values['year'],
    'value_formatter': "xapian.sortable_serialise(float(%s))"  % field_value,
    'value_range_search' : True,
    'value_range_prefix' : 'year:',
    'formatter' : "scheme.calc_year(%s)" % field_value,
    'doc_body' : True,
  }

  fields['amount'] = {
    'value' : fsconf.index_values['amount'],
    'value_formatter': "xapian.sortable_serialise(float(%s))"  % field_value,
    'value_range_search' : True,    
    'value_range_prefix' : 'amount:',
    'doc_body' : True,
  }

  fields['total_amount'] = {
    'value' : fsconf.index_values['total_amount'],
    'value_formatter': "xapian.sortable_serialise(float(%s))"  % field_value,
    'value_range_search' : True,    
    'value_range_prefix' : 'totalamount:',
    'doc_body' : True,
  }


  fields['country'] = {
    'prefix' : 'XCOUNTRY:',
    'name' : 'country',
    'boolean' : True,
    'doc_body' : True,
    'geo_weight' : 0,
  }

  fields['recipient_id'] = {
    'prefix' : 'XRID:',
    'name' : 'id',
    'doc_body' : True,
  }

  fields['recipient_id_x'] = {
    'prefix' : 'XRIDX',
    'name' : 'xid',
    'value' : fsconf.index_values['recipient_id_x'],
    'value_formatter': "%s"  % field_value,
    'doc_body' : True,
  }

  fields['geo1'] = {
    'index' : True,
    'termweight' : 50,
    'doc_body' : True,
    'geo_weight' : 1,
  }



  fields['geo2'] = {
    'index' : True,
    'termweight' : 40,
    'doc_body' : True,
    'geo_weight' : 2,
  }

  fields['geo3'] = {
    'index' : True,
    'termweight' : 30,
    'doc_body' : True,
    'geo_weight' : 3,
  }

  fields['geo4'] = {
    'index' : True,
    'termweight' : 20,
    'doc_body' : True,
    'geo_weight' : 4,
  }

  fields['town'] = {
    'index' : True,
    'termweight' : 10,
    'doc_body' : True,
    'geo_weight' : 5,
  }

  fields['town1'] = {
    'index' : True,
    'termweight' : 10,
    'doc_body' : True,
    'geo_weight' : 6,
  }

  fields['town2'] = {
    'index' : True,
    'termweight' : 10,
    'doc_body' : True,
    'geo_weight' : 7,
  }

  fields['town3'] = {
    'index' : True,
    'termweight' : 10,
    'doc_body' : True,
    'geo_weight' : 8,
  }

  fields['geopath'] = {
  'doc_body' : True,
  'prefix' : 'XGEOPATH:',
  'name' : 'geopath',
  'boolean' : True,
  }

  fields['lat'] = {
  'doc_body' : True,
  'name' : 'lat',
  }

  fields['long'] = {
  'doc_body' : True,
  'name' : 'long',
  }

  fields['scheme_name'] = {
    'prefix' : 'XSCHEME:',
    'name' : 'scheme',
    'termweight' : 500,
    'index' : True,
    'doc_body' : True,
  }


  return fields
  
