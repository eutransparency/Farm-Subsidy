# encoding: utf-8
from django.db import models
from django.db import connection, backend, models
from indexer import countryCodes
import fsconf


DEFAULT_YEAR = fsconf.default_year

"""
Various SQL queries.  Accessable via models.data.objects.[functionname]

TODO: There is loads of boilerplating going on here (extra_and building,
returning rows etc). I need to figure out a way to make this better...

"""

class FarmDataManager(models.Manager):
  
  
  def years(self, country=None, scheme=None, location={'name' : None}):
    
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND country = '%s'" % country
    
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT year as y
      FROM data_years 
      WHERE year IS NOT NULL %(extra_and)s
      GROUP BY y
      ORDER BY y ASC 
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0])
        result_list.append(p)
    return result_list
    
  
  def top_recipients(self, country=None, year=DEFAULT_YEAR, limit=5):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND t.countrypayment = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND year='%s'" % year
      
    cursor = connection.cursor()
    cursor.execute("""
      SELECT max(t.nameenglish), SUM(t.amount_euro), MAX(t.global_id) 
      FROM data_totals t
      WHERE t.nameenglish IS NOT NULL %(extra_and)s
      GROUP BY t.global_id
      ORDER BY SUM(t.amount_euro) DESC LIMIT %(limit)s;
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(name=row[0], amount_euro=row[1], globalrecipientidx=row[2])
        result_list.append(p)
    return result_list
  
  
  def top_schemes(self, country=None, year=DEFAULT_YEAR, limit=5):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND country = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND year='%s'" % year
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT name, '', amount as total, globalschemeid, country
    FROM data_scheme_totals
    WHERE amount IS NOT NULL %(extra_and)s
    ORDER BY total DESC
    LIMIT %(limit)s
    """ % locals())

    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro=row[2], globalschemeid=row[3], country=row[4])
      if row[1]:
        p.name = row[1]
      else:
        p.name = row[0]
      result_list.append(p)
    return result_list
  
  def top_regions(self, country=None, year=DEFAULT_YEAR, limit=5):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND p.countrypayment = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND p.year='%s'" % year
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT LOWER(r.geo1) as G, SUM(p.amounteuro) as total FROM data_recipients r
    JOIN data_payments p
    ON r.globalrecipientidx = p.globalrecipientidx
    WHERE r.geo1 IS NOT NULL %(extra_and)s
    GROUP BY G
    ORDER BY total DESC
    LIMIT %(limit)s
    """ % locals())

    result_list = []
    for row in cursor.fetchall():
      p = self.model(name = row[0], amount_euro=row[1])
      result_list.append(p)
    return result_list
  
  def amount_years(self, country=None, scheme=None):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND countrypayment = '%s'" % country    
    if scheme:
      extra_and += " AND globalschemeid = '%s'" % scheme
    cursor = connection.cursor()
    cursor.execute("""
    SELECT SUM(amounteuro), year
    FROM data_payments p
    WHERE year IS NOT NULL %(extra_and)s
    GROUP BY year
    ORDER BY year ASC
    """ % locals())

    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro = row[0], year=row[1])
      result_list.append(p)
    return result_list
    
    
  def browse_recipients(self, country, year, sort='amount', scheme=None, location=(), limit=10):
    extra_and = ""
    if country and country != "EU":
      if scheme:
        extra_and += " AND p.countrypayment = '%s'" % country    
      else:
        extra_and += " AND countrypayment = '%s'" % country    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    

    if limit is not None:
      limit = "LIMIT %s" % limit
    else:
      limit = ""
      

    cursor = connection.cursor()  
      
    if scheme:
      cursor.execute("""
      SELECT SUM(p.amounteuro) as E, MAX(r.name), r.globalrecipientidx FROM 
      data_recipients r
      JOIN data_payments p ON
      r.globalrecipientidx = p.globalrecipientidx
      WHERE p.globalschemeid = '%(scheme)s' %(extra_and)s
      GROUP BY r.globalrecipientidx
      ORDER BY E DESC
      %(limit)s
      """ % locals())
    elif location:
      cursor.execute("""
      SELECT SUM(p.amounteuro) as E, MIN(r.name), MAX(r.countryrecipient) 
      FROM data_recipients r
      JOIN data_payments p
      ON r.globalrecipientidx=p.globalrecipientidx
      WHERE LOWER(r.geo1)='tirol' AND p.countrypayment='AT'
      GROUP BY r.globalrecipientidx
      ORDER BY E DESC
      %(limit)s
      """ % locals())
    else: 
      cursor.execute("""
      SELECT SUM(amount_euro) as E, MAX(nameenglish), global_id
      FROM data_totals
      WHERE nameenglish IS NOT NULL %(extra_and)s
      GROUP BY global_id
      ORDER BY E DESC
      """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro = row[0], name=row[1], globalrecipientidx=row[2])
      result_list.append(p)
    return result_list



  def browse_schemes(self, country, year, sort):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND country = '%s'" % country    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT amount, name, globalschemeid
    FROM data_scheme_totals
    WHERE name IS NOT NULL %(extra_and)s
    ORDER BY amount DESC
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro = row[0], name=row[1])
      p.globalschemeid = row[2]
      result_list.append(p)
    return result_list

  def browse_location(self, country, year, parent=None, sort='amount'):
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND p.countrypayment = '%s'" % country    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    
    
    field = 'geo1'
    if parent == 'geo1':
      field = 'geo2'
    
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT LOWER(r.%(field)s) as G, SUM(p.amounteuro) as total FROM data_recipients r
    JOIN data_payments p
    ON r.globalrecipientidx = p.globalrecipientidx
    WHERE r.geo1 IS NOT NULL %(extra_and)s
    GROUP BY G
    ORDER BY total DESC
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(name = row[0], amount_euro=row[1])
      result_list.append(p)
    return result_list

  


class LocationManager(models.Manager):
  
  def location_years(self, country=None, name=None, parent={'country' : None}):
    
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND country = '%s'" % country

    # name = smart_unicode(name)
    print name
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT year as y
      FROM data_locations 
      WHERE year IS NOT NULL AND name='%(name)s' %(extra_and)s
      GROUP BY y
      ORDER BY y ASC 
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(year=row[0])
        result_list.append(p)
    return result_list



  def locations(self, country="EU", parent=None, year=DEFAULT_YEAR, limit=10):
    
    if country == "EU":
      countries = countryCodes.country_codes()
    else:
      countries = [country]
    countries = ",".join("'%s'" % country for country in countries)
    
    if parent == None or parent == "EU":
      parent = [code.lower() for code in countryCodes.country_codes()]
    else:
      parent = [parent.lower()]

    parents = ",".join("'%s'" % country for country in parent)    
    extra_and = ""
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    
    
    if limit is not None:
      limit = "LIMIT %s" % limit
    else:
      limit = ""

    cursor = connection.cursor()
    sql = """
    SELECT t.geo1 as name, MIN(l.total) as total, l.country, MAX(t.N) AS count, (l.total/t.N) AS avg
    FROM (
      SELECT COUNT(*) AS N, geo1 
      FROM data_recipients 
      GROUP BY geo1
      ) AS t
    JOIN (
      SELECT SUM(total) as total, name, country 
      FROM data_locations 
      WHERE country IN (%(countries)s) 
      AND parent_name IN (%(parents)s) 
      AND name != parent_name
      %(extra_and)s 
      GROUP BY name, country
      )  AS l
    ON l.name=t.geo1
    GROUP BY t.geo1, avg, l.country
    ORDER BY total DESC      
    %(limit)s
    """ % locals()
    cursor.execute(sql)
    
    result_list = []
    for row in cursor.fetchall():
      print dir(self.model)
      p = self.model(name=row[0], total=row[1], country=row[2])
      p.count = row[3]
      p.avg = row[4]
      result_list.append(p)
    return result_list
    
    
