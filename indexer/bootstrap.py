#!/usr/bin/env python
# encoding: utf-8

"""
bootstrap.py

Created by Sym on 2009-08-02.

Does the initial loading of the databases.

"""

import connection


def load_scheme():
  """Excicutes the SQL in scheme.sql"""
  
  # exit = raw_input("""WARNING: This will destroy any existing data that may be 
  # in the database.  Do you want to continue?\n[Y/n]:""")
  # if len(exit) > 0 and exit[0] == "n":
  #   print "Exiting"
  #   sys.exit()
  
  
  conn, c = connection.connect()
  
  f = open('scheme.sql', 'r')
  c.execute(f.read())
  conn.commit()

if __name__ == "__main__":
 load_scheme()