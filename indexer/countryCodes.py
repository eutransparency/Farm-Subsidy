#!/usr/bin/env python
# encoding: utf-8


def countryCodes():
  codes = []
  codes.append('AT')
  codes.append('BE')
  codes.append('BG')
  codes.append('CZ')
  codes.append('AT')
  codes.append('EE')
  codes.append('FR')
  codes.append('DE')
  codes.append('HU')
  codes.append('IE')
  codes.append('IT')
  codes.append('LV')
  codes.append('LT')
  codes.append('PL')
  codes.append('PT')
  codes.append('S')  
  codes.append('SK')
  codes.append('SL')
  codes.append('ES')
  codes.append('UK')
  return codes


def filenameToCountryCode(filename):
  if filename[0:7] == 'austria':
    return 'AT'
  if filename[0:7] == 'belgium':
    return 'BE'
  if filename[0:8] == 'bulgaria':
    return 'BG'
  if filename[0:5] == 'czech':
    return 'CZ'
  if filename[0:7] == 'estonia':
    return 'EE'
  if filename[0:7] == 'finland':
    return 'FI'
  if filename[0:6] == 'france':
    return 'FR'
  if filename[0:7] == 'germany':
    return 'DE'
  if filename[0:7] == 'hungary':
    return 'HU'
  if filename[0:7] == 'ireland':
    return 'IE'
  if filename[0:5] == 'italy':
    return 'IT'
  if filename[0:6] == 'latvia':
    return 'LV'
  if filename[0:9] == 'lithuania':
    return 'LT'
  if filename[0:10] == 'netherland':
    return 'NL'        
  if filename[0:6] == 'poland':
    return 'PL'
  if filename[0:8] == 'portugal':
    return 'PT'
  if filename[0:8] == 'slovakia':
    return 'SK'
  if filename[0:8] == 'slovenia':
    return 'SL'
  if filename[0:5] == 'spain':
    return 'ES'
  if filename[0:13] == 'unitedkingdom':
    return 'UK'
  else:
    raise Exception, "Could not work out country for %s!" % filename
  
if __name__ == '__main__':
  print countryCodes()

