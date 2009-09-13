#!/usr/bin/env python
# encoding: utf-8

import os
import sys
# sys.path.append("/".join(sys.path[0].split('/')[:-1]))

#Set up Paths

#Path to root of the project (where the indexer is),
project_path = '/var/www/farmsubsidy/'

# absolute path to the data (folder containing mdb and csv folders)
datadir = project_path + "data"

# Tmp path
tmppath = "/tmp"

#Indexer path
indexer_path = project_path + "indexer"

#Path to the MDBs (from unzipped data)
mdbdir = datadir + "/mdb"

#Path to the stats
statsdir = datadir + "/stats"

#Path to the CSV files (from MDBs)
csvdir = datadir + "/csv"

#Path to scheme directory
schemedir = datadir+'/scheme/'

#Xapian Database
xapianDbPath = project_path + 'xapian.db'

#Xapian cache path
xapcache_path = '/tmp/xapcache.sqlite'

#Mysql database name to use to temp databases
mysql_prefix = "farmsubsidy_"
mysql_user = "farmsubsidy"
mysql_pass = "farmsubsidy"

current_year = "2007"


# Xapian database values
index_values = {
  'global_id' :         0,
  'global_id_x' :       1,
  'recipient_id' :      2,
  'recipient_id_x' :    3,  
  'year' :              4,
  'amount' :            5,
  'total_amount' :      6,  
}


default_year = 2008