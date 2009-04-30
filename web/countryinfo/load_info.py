import csv
import re
import locale
locale.setlocale(locale.LC_ALL, '')

from farmsubsidy import fsconf

def load_info(country=None, format=True, year=fsconf.current_year):
  filepath = "%s/%s/basic_comparisons.csv" % (fsconf.statsdir, year)
  stats = csv.DictReader(open(filepath, "U"))
  if country:
    for row in stats:
      if row['Country'] == country:
        info = row
      
        # delete unwanted elements
        del info['Country']
        del info['Population']
        del info['']
        
        if format:
          # Format elements
          for k,v in info.items():
            try:
              info[k] = locale.format('%.0f', float(info[k]), True)
            except:
              pass

          info['Total spending'] += " Million Euros"
          info['Total contribution'] += " Million Euros"
          info['Contribution per citizen'] = "&euro;%s" % info['Contribution per citizen']
          info['Spending per citizen'] = "&euro;%s" % info['Spending per citizen']
          
          info['Spending per hectare'] = "&euro;%s" % info['Spending per hectare']
          info['Spending per farm'] = "&euro;%s" % info['Spending per farm']
          info['Spending per farm worker'] = "&euro;%s" % info['Spending per farm worker']
          
          info['Proportion of payments to top 10%'] += "%"
          info['Proportion of payments to top 20%'] += "%"
          
          # info_sorted = []
          for key, value in info.items():
            del info[key]
            key = re.sub(" ", "_", key.lower())
            key = re.sub("%", "", key)
            info[key] = value
          
        return info
  else:
    return stats



if __name__ == "__main__":
  info = load_info("UK")
  for k,v in info:
    print k,v