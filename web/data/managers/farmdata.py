# encoding: utf-8
from django.db import models
from django.db import connection, backend, models
import re
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
    # if year and str(year) != "0":
    #   extra_and += " AND year='%s'" % year
    cursor = connection.cursor()
    cursor.execute("""
      SELECT t.nameenglish, t.amount_euro AS T, t.global_id, t.countrypayment
      FROM data_totals t
      WHERE t.nameenglish IS NOT NULL
      AND year=%(year)s %(extra_and)s
      ORDER BY T DESC LIMIT %(limit)s;
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
        p = self.model(name=row[0], amount_euro=row[1], globalrecipientidx=row[2], country=row[3])
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
      extra_and += " AND country = '%s'" % country    
      table = "data_years"
    if scheme:
      extra_and += " AND globalschemeid = '%s'" % scheme
      table = "data_scheme_totals"
    
    sql = """
      SELECT SUM(amount), year
      FROM %(table)s y
      WHERE year IS NOT NULL %(extra_and)s
      GROUP BY year
      ORDER BY year ASC
      """ % locals()
    cursor = connection.cursor()
    cursor.execute(sql)

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
    else: 
      cursor.execute("""
      SELECT amount_euro AS E, nameenglish, global_id
      FROM data_totals
      WHERE nameenglish IS NOT NULL %(extra_and)s
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

  def recipient_payments(self, globalrecipientidx, group=False):
    
    if group:
      sql = """
        SELECT SUM(p.amounteuro), p.year, MAX(s.nameenglish), MAX(s.globalschemeid), p.countrypayment
        FROM data_payments p 
        JOIN data_schemes s
        ON p.globalschemeid=s.globalschemeid
        WHERE p.globalrecipientidx='%(globalrecipientidx)s' 
        GROUP BY p.year, p.countrypayment
        ORDER BY p.year ASC
      """ % locals()
    else:
      sql = """
        SELECT SUM(p.amounteuro), p.year, s.nameenglish, MAX(s.globalschemeid), p.countrypayment
        FROM data_payments p 
        JOIN data_schemes s
        ON p.globalschemeid=s.globalschemeid
        WHERE p.globalrecipientidx='%(globalrecipientidx)s' 
        GROUP BY p.year, s.nameenglish, p.countrypayment
        ORDER BY p.year ASC
      """ % locals()

    cursor = connection.cursor()
    cursor.execute(sql)
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro=row[0], year=row[1], name=row[2], country=row[4])
      p.schemeid = row[3]
      result_list.append(p)
    return result_list





class LocationManager(models.Manager):
  
  def location_years(self, country=None, name=None, parent={'country' : None}):
    
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND country = '%s'" % country

    name = re.sub("'","\\'",name)
    
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



  def locations(self, country="EU", parent=None, name=None, year=DEFAULT_YEAR, limit=10, sort='amount'):
    if country == "EU":
      countries = countryCodes.country_codes()
    else:
      countries = [country]
    countries = ",".join("'%s'" % country for country in countries)
    
    if parent == None or parent == "EU":
      parent = [code.lower() for code in countryCodes.country_codes()]
    else:
      parent = [parent.lower()]
     
    parents = r",".join(r"'%s'" % re.sub("'","\\'", location) for location in parent)    
    extra_and = ""
    
    if name:
        extra_and += " AND name='%s'" % re.escape(name)
    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    
    
    if limit is not None:
      limit = "LIMIT %s" % limit
    else:
      limit = ""
    
    if sort == 'avg':
        sort_by = 'avg DESC'
    elif sort == 'recipients':
        sort_by = 'r DESC'
    elif sort == 'name':
        sort_by = 'name ASC'
    else:
        sort_by = 't DESC'
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *, A.t/A.r as avg FROM
    (SELECT name, SUM(total) AS t, country, MAX(recipients) as r, latlng::varchar as ll
    FROM data_locations
    WHERE country IN (%(countries)s) 
    AND parent_name IN (%(parents)s) 
    AND name NOT IN (LOWER(%(countries)s))
    %(extra_and)s
    GROUP BY ll, name, country
    %(limit)s) as A
    ORDER BY %(sort_by)s
    """ % locals())
    result_list = []
    for row in cursor.fetchall():
      p = self.model(name=row[0], total=row[1], country=row[2])
      p.count = row[3]
      try:
          p.latlng = row[4][1:-1]
      except:
          p.latlng = []
          
      p.avg = row[5]
      result_list.append(p)
    return result_list
    
    
  def recipients_by_location(self, country, location, year=0, limit=10, offset=0):
    
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM 
        (SELECT DISTINCT ON (t.global_id) * FROM
            (SELECT global_id, MAX(location), MAX(country) FROM data_recipient_locations
            WHERE location='%(location)s'
            GROUP BY global_id
            LIMIT %(limit)s
            OFFSET %(offset)s) as r
        join data_totals t
        ON t.global_id=r.global_id) as l
    ORDER BY l.amount_euro DESC
    """% {'location' : re.sub("'", "\\'", location), 'limit' : limit, 'offset' : offset})
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(name=row[7])
      p.amount_euro = row[4]
      p.global_id = row[0]
      result_list.append(p)
    return result_list
    
    
    
    
    