#!/usr/bin/env python
# encoding: utf-8

import os

#Set up Paths

#Path to root of the project (where the indexer is),
# if os.environ['COMPUTERNAME'] == "macbook-sym":
#project_path = "/Users/sym/Projects/farm-subsidy/"
# else:
project_path = "/var/www/farmsubsidy/"

# absolute path to the data (folder containing mdb and csv folders)
datadir = project_path + "data"

# Tmp path
tmppath = "/tmp"

#Indexer path
indexer_path = project_path + "indexer"

#Path to the MDBs (from unzipped data)
mdbdir = datadir + "/mdb"

#Path to the CSV files (from MDBs)
csvdir = datadir + "/csv"

#Path to scheme directory
schemedir = datadir+'/scheme/'

#Xapian Database
xapianDbPath = project_path + 'xapian.db'

#Mysql database name to use to temp databases
mysql_prefix = "farmsubsidy_"
mysql_user = "farmsubsidy2"
mysql_pass = "farmsubsidy"


# Xapian database values
index_values = {
  'docid' : 0,
  'year' : 1,
  'amount' : 2
}
