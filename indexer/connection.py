#!/usr/bin/env python
# encoding: utf-8

"""
connection.py

Created by Sym on 2009-08-02.

Manages connections to the farmsubsidy database, for use by the indexing scripts.

"""
import psycopg2
from config import *
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('pgloader.conf')

HOST = config.get('pgsql', 'host')
PORT = config.get('pgsql', 'port')
DBNAME = config.get('pgsql', 'base')
USER = config.get('pgsql', 'user')
PASSWORD = config.get('pgsql', 'pass')
                              
def connect():                
  conn = psycopg2.connect(
    "dbname='%(dbname)s' user='%(user)s' host='%(host)s' port=%(PORT)s password='%(password)s'" 
    % {
      'dbname' : DBNAME, 
      'user' : USER, 
      'host' : HOST, 
      'password' : PASSWORD, 
      'PORT' : PORT, 
    })
  cur = conn.cursor()
  return conn, cur


if __name__ == "__main__":
  conn, cur = connect()
  print conn, cur
