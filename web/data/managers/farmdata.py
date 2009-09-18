from django.db import models
from django.db import connection, backend, models

from farmsubsidy import fsconf

DEFAULT_YEAR = fsconf.default_year

"""
Various SQL queries.  Accessable via models.data.objects.[functionname]

TODO: There is loads of boilerplating going on here (extra_and building,
returning rows etc). I need to figure out a way to make this better...

"""

class FarmDataManager(models.Manager):
  
  
  def years(self, country=None, scheme=None):
    
    extra_and = ""
    if country and country != "EU":
      extra_and += " AND countrypayment = '%s'" % country
    
    
    cursor = connection.cursor()
    cursor.execute("""
      SELECT year as y
      FROM data_payments p 
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
      extra_and += " AND p.countrypayment = '%s'" % country
    if year and str(year) != "0":
      extra_and += " AND p.year='%s'" % year
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT MAX(s.nameenglish), MAX(s.budgetlines8digit), SUM(p.amounteuro) as total, s.globalschemeid
    FROM data_schemes s
    JOIN data_payments p
    ON s.globalschemeid = p.globalschemeid
    WHERE p.amounteuro IS NOT NULL %(extra_and)s
    GROUP BY s.globalschemeid
    ORDER BY total DESC
    LIMIT %(limit)s
    """ % locals())

    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro=row[2], globalschemeid=row[3])
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
    SELECT r.geo1, SUM(p.amounteuro) as total FROM data_recipients r
    JOIN data_payments p
    ON r.globalrecipientidx = p.globalrecipientidx
    WHERE r.geo1 IS NOT NULL %(extra_and)s
    GROUP BY r.geo1
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
    
    
  def browse_recipients(self, country, year, sort='amount', scheme=None, limit=10):
    extra_and = ""
    if country and country != "EU":
      if scheme:
        extra_and += " AND p.countrypayment = '%s'" % country    
      else:
        extra_and += " AND countrypayment = '%s'" % country    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    

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
      LIMIT %(limit)s
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
      extra_and += " AND p.countrypayment = '%s'" % country    
    if year and int(year) != 0:
      extra_and += " AND year = '%s'" % year    
    
    cursor = connection.cursor()
    cursor.execute("""
    SELECT SUM(p.amounteuro) as E, MAX(s.nameenglish)
    FROM data_payments p
    JOIN data_schemes s
    ON (p.globalschemeid = s.globalschemeid)
    WHERE s.nameenglish IS NOT NULL %(extra_and)s
    GROUP BY s.globalschemeid
    ORDER BY E DESC
    """ % locals())
    
    result_list = []
    for row in cursor.fetchall():
      p = self.model(amount_euro = row[0], name=row[1])
      result_list.append(p)
    return result_list
