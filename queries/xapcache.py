#!/usr/bin/env python
# encoding: utf-8

import sqlite3
import cPickle
import sys
import hashlib

def _create_or_open():
  """Creates and/or opens a sqlite database"""
  conn = sqlite3.connect('/tmp/xapcache.sqlite')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS cache (query text PRIMARY KEY, results blob)''')
  return conn,c
  
def load_cache(query, options):
  conn,c = _create_or_open()
  sql = '''SELECT results FROM cache WHERE query=?'''
  query = hashlib.sha224("%s%s" % (query, str(options))).hexdigest()
  results = c.execute(sql, (query,))
  try:
    result = results.fetchone()
    return cPickle.loads(str(result[0]))
  except:
    return None
  
def save_cache(query, options, results):
  conn,c = _create_or_open()
  results = cPickle.dumps(results)
  query = hashlib.sha224("%s%s" % (query, str(options))).hexdigest()
  sql = '''INSERT OR REPLACE INTO cache VALUES (?,?)'''
  c.execute(sql, (query,results,))  
  conn.commit()


if __name__ == "__main__":
  save_cache('foo', 'bar')
  load_cache('foo')
  
  