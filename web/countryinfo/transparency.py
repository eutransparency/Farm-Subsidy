import csv
import sys

from data import countryCodes
from django.conf import settings

def open_index():
  filepath = "%s/transparency/index.csv" % (settings.STATS_DIR)
  return csv.reader(open(filepath, "U"))
  
def transparency_score(country):
  index = open_index()
  for i,row in enumerate(index):
    if row[0] == country:
      i = i+1
      if 4 <= i <= 20 or 24 <= i <= 30:
          suffix = "th"
      else:
          suffix = ["st", "nd", "rd"][i % 10 - 1]
      
      return {'rank' : "%s%s" % (i, suffix),'percent' : row[1]}

def transparency_list():
  index = open_index()
  table = []
  for row in index:
    table.append((countryCodes.code2name[row[0]], row[1]))
  return table
  


if __name__ == "__main__":
  print sys.argv[1]
  print transparency_score(sys.argv[1])
