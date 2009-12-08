#!/usr/bin/env python
# encoding: utf-8

"""
connection.py

Created by Sym on 2009-08-02.

Manages connections to the farmsubsidy database, for use by the indexing scripts.

"""
import psycopg2
from config import *


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
