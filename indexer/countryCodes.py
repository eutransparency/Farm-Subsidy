#!/usr/bin/env python
# encoding: utf-8


def countryCodes():
  codes = []
  codes.append('AT')
  codes.append('BE')
  codes.append('BG')
  codes.append('CZ')
  codes.append('DE')
  codes.append('DK')
  codes.append('EE')
  codes.append('ES')
  codes.append('FI')
  codes.append('FR')
  codes.append('GR')
  codes.append('HU')
  codes.append('IE')
  codes.append('IT')
  codes.append('LT')
  codes.append('MT')
  codes.append('LU')
  codes.append('LV')
  codes.append('NL')
  codes.append('PL')
  codes.append('PT')
  codes.append('RO')
  codes.append('SE')    
  codes.append('SK')
  codes.append('SL')
  codes.append('GB')
  return codes


code2name = {
'AT'	:	'Austria',
'BE'	:	'Belgium',
'BG'	:	'Bulgaria',
'CZ'	:	'Czech',
'DK'	:	'Denmark',
'EE'	:	'Estonia',
'FI'	:	'Finland',
'FR'	:	'France',
'DE'	:	'Germany',
'GR'	:	'Greece',
'HU'	:	'Hungary',
'IE'	:	'Ireland',
'IT'	:	'Italy',
'LV'	:	'Latvia',
'LT'	:	'Lithuania',
'LU'	:	'Luxembourg',
'MT'	:	'Malta',
'NL'	:	'Netherland',
'PL'	:	'Poland',
'PT'	:	'Portugal',
'RO'	:	'Romaina',
'SK'	:	'Slovakia',
'SL'	:	'Slovenia',
'ES'	:	'Spain',
'SE'	:	'Sweden',
'GB'	:	'United Kingdom',
}

def filenameToCountryCode(filename):
  if filename[0:7] == 'austria':
    return 'AT'
  if filename[0:7] == 'belgium':
    return 'BE'
  if filename[0:8] == 'bulgaria':
    return 'BG'
  if filename[0:5] == 'czech':
    return 'CZ'
  if filename[0:7] == 'denmark':
    return 'DK'
  if filename[0:7] == 'estonia':
    return 'EE'
  if filename[0:7] == 'finland':
    return 'FI'
  if filename[0:6] == 'france':
    return 'FR'
  if filename[0:7] == 'germany':
    return 'DE'
  if filename[0:6] == 'greece':
    return 'GR'
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
  if filename[0:10] == 'luxembourg':
    return 'LU'
  if filename[0:5] == 'matla':
    return 'MT'
  if filename[0:10] == 'netherland':
    return 'NL'        
  if filename[0:6] == 'poland':
    return 'PL'
  if filename[0:8] == 'portugal':
    return 'PT'
  if filename[0:3] == 'rom':
    return 'ROM'
  if filename[0:8] == 'slovakia':
    return 'SK'
  if filename[0:8] == 'slovenia':
    return 'SL'
  if filename[0:5] == 'spain':
    return 'ES'
  if filename[0:6] == 'sweden':
    return 'SE'
  if filename[0:13] == 'unitedkingdom':
    return 'GB'
  else:
    raise Exception, "Could not work out country for %s!" % filename
  
if __name__ == '__main__':
  print countryCodes()

