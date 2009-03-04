#!/usr/bin/env python
# encoding: utf-8
"""
mappings.py
"""

import fsconf
import collections


def fieldTypeMaps(field_value='field_value'):
  """Defines how different fields should be indexed and queried by xapian, including prefixes and values"""
  
  fields = collections.defaultdict(dict)
  
  fields['name'] = {
    'prefix' : 'XNAME',
    'name' : 'name',
    'termweight' : 100,
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

  fields['country'] = {
    'prefix' : 'XCOUNTRY:',
    'name' : 'country',
    'boolean' : True,
    'doc_body' : True,
  }

  fields['recipient_id'] = {
    'prefix' : 'XRID:',
    'name' : 'id',
    'value' : fsconf.index_values['recipient_id'],
    'value_formatter': "%s"  % field_value,
    'doc_body' : True,
  }

  fields['recipient_id_x'] = {
    'prefix' : 'XRIDX:',
    'name' : 'xid',
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
  
