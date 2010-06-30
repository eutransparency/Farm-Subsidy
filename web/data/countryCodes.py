import sys
from django.utils.datastructures import SortedDict


def country_codes(code=None, local='GB'):
  countries = SortedDict()
  countries['EU']	=	{'GB' : 'All Countries'}
  countries['AT']	=	{'GB' : 'Austria'}
  countries['BE'] = {'GB' : 'Belgium'}
  countries['BG']	=	{'GB' : 'Bulgaria'}
  countries['CY']	=	{'GB' : 'Cyprus'}
  countries['CZ']	=	{'GB' : 'Czech Republic'}
  countries['DK']	=	{'GB' : 'Denmark'}
  countries['EE']	=	{'GB' : 'Estonia'}
  countries['FI']	=	{'GB' : 'Finland'}
  countries['FR']	=	{'GB' : 'France'}
  countries['DE']	=	{'GB' : 'Germany'}
  countries['GR']	=	{'GB' : 'Greece'}
  countries['HU']	=	{'GB' : 'Hungary'}
  countries['IT']	=	{'GB' : 'Italy'}
  countries['IE']	=	{'GB' : 'Ireland'}
  countries['LV']	=	{'GB' : 'Latvia'}  
  countries['LT']	=	{'GB' : 'Lithuania'}
  countries['LU']	=	{'GB' : 'Luxembourg'}
  countries['MT']	=	{'GB' : 'Malta'}
  countries['NL']	=	{'GB' : 'Netherlands'}
  countries['PO']	=	{'GB' : 'Poland'}
  countries['PT']	=	{'GB' : 'Portugal'}
  countries['RO']	=	{'GB' : 'Romania'}
  countries['SK']	=	{'GB' : 'Slovakia'}  
  countries['SL']	=	{'GB' : 'Slovenia'}
  countries['ES']	=	{'GB' : 'Spain'}
  countries['SE']	=	{'GB' : 'Sweden'}  
  countries['GB']	=	{'GB' : 'United Kingdom'}
  
  
  if code:
    if code in countries.keys():
      return {'code' : code, 'name' : countries[code][local]}
    else:
      raise ValueError, "%s not a country" % code
  else:
    return countries.keys()

if __name__ == "__main__":
  print country_codes()