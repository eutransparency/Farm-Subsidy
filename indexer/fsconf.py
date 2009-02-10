#!/usr/bin/env python
# encoding: utf-8

import os

#Set up Paths

#Path to root of the project (where the indexer is)
if os.environ['COMPUTERNAME'] == "macbook-sym":
  project_path = "/Users/sym/Projects/farm-subsidy"
else:
  project_path = "/var/www/farmsubsidy"

#Indexer path
indexer_path = project_path + "indexer"

# Absolute path to the data (folder containing mdb and csv folders)
if os.environ['COMPUTERNAME'] == "macbook-sym":
  datadir = "/Users/sym/Projects/farm-subsidy/data"
else:
  datadir = "/var/www/farmsubsidy/data"

#Path to the MDBs (from unzipped data)
mdbdir = datadir + "/mdb"

#Path to the CSV files (from MDBs)
csvdir = datadir + "/csv"

#Path to scheme directory
schemedir = datadir+'/scheme/'

#Xapian Database
xapianDbPath = project_path + '/xapian.db'
