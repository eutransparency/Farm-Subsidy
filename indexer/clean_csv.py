"""
Used redis to remove duplicated rows from a CSV file.

Duplicates are identified by a selected field in the row tuple, rather than all
fields.

In cases where more than one field needs to be checked for duplicates, the file
will need to be run through the script n times


Usage: By default the first field in the csv file is used.  If you want to
change this, pass --field (or -f) followed by an int.

The other two (required) options are --in and --out, and should be self
explanitry!

A Redis server and the python redis client is required.

"""

import sys
from optparse import OptionParser
import csv
import StringIO

import redis

parser = OptionParser()
parser.add_option("-f", "--field", 
                  dest="field", default=0, type="int",
                  help="(int) Duplicate field offset")
parser.add_option("-i", "--in", 
                  dest="IN_FILE", 
                  help="Path to the input file.")
parser.add_option("-o", "--out", 
                  dest="OUT_FILE", 
                  help="Path to the output file.")
parser.add_option("-s", "--same-as", 
                  dest="SAME_AS", type="int", 
                  help="""(int) Only add lines where [duplicate field] is the same as
                  this.""")



(options, args) = parser.parse_args()

r = redis.Redis()
ID_FIELD = options.field
SAME_AS = options.SAME_AS

try:
    in_file = csv.reader(open(options.IN_FILE), delimiter=';')
except:
    raise Exception('Input file not found')

if options.OUT_FILE:
    out_file = open(options.OUT_FILE, 'w')
else:
    out_file = open("%s.out" % options.IN_FILE, 'w')

key_prefix = "csv-clean-%s" % options.IN_FILE.replace('/', '-')
r.delete(key_prefix)
deleted = 0

def process_line(line):
    s = StringIO.StringIO()
    w = csv.writer(s, delimiter=';')
    w.writerow(line)
    return r.hset(key_prefix, line[ID_FIELD], s.getvalue())
    # return  r.hdel(key_prefix, line[ID_FIELD])


print "Removing Duplicates"
for line in in_file:
    if SAME_AS:
        print line[SAME_AS], line[ID_FIELD]
        if line[SAME_AS] == line[ID_FIELD]:
            deleted += process_line(line)
    else:
        deleted += process_line(line)


print "Deleted %s rows, writing %s lines to out file" % (deleted,
                                                         r.hlen(key_prefix))

for row in r.hvals(key_prefix):
    out_file.write(row)


r.delete(key_prefix)


