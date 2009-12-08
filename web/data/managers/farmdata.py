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


  def location(self, country, geo1=None, geo2=None, geo3=None, geo4=None):
      columns_available = [('country',country),('geo1', geo1), ('geo2', geo2), ('geo3', geo3), ('geo4', geo4)]
      sql_where = []
      location = None
      for i in columns_available:
          if i[1] is not None:
              location = i
              sql_where.append("%s='%s'" % i)
          else:
              sql_where.append("%s IS NULL" % i[0])
      location_type = location[0]
      where_str = " AND ".join(sql_where)
      
      cursor = connection.cursor()
      cursor.execute("""
      SELECT * FROM data_locations
      WHERE %(where_str)s
      AND location_type = '%(location_type)s'
      LIMIT 1
      """ % locals())

      result_list = []
      for row in cursor.fetchall():
        p = self.model()
        p.location_type = row[0]
        p.country=row[1]
        p.geo1=row[2]
        p.geo2=row[3]
        p.geo3=row[4]
        p.geo4=row[5]
        p.recipients=row[6]
        p.total=row[7]

        p.name=p.__dict__.get(p.location_type, '')

        result_list.append(p)
      try:
          return result_list[0]
      except:
          pass

  def sub_locations(self, country="EU", geo1=None,geo2=None,geo3=None,geo4=None, limit=10, sort='amount'):
    if country == "EU":
      countries = countryCodes.country_codes()
    else:
      countries = [country]
    countries = ",".join("'%s'" % country for country in countries)

    columns_available = [('geo1', geo1), ('geo2', geo2), ('geo3', geo3), ('geo4', geo4)]

    if geo1:
        if not geo4:
            # Find the first value that is None, and assign that to 'child'
            child_columns = columns_available[:]
            child = None
            while not child:
                i = child_columns.pop(0)
                if i[1] == None:
                    child = i
        else:
            # There can be no sub-locations for geo4
            return []
    
        columns_used = []
        sql_where = []
        group_by = []
        for i in columns_available:
            if i[1]:
                # This geo exists
                columns_used.append(i[0])
                sql_where.append(i)
                group_by.append(i[0])
            else:
                # This one doesn't
                if i[0] == child[0]:
                    columns_used.append(child[0])
                else:
                    columns_used.append('NULL')
                
        group_by.append(child[0])
        columns_str = ",".join(columns_used)
        group_by.reverse()
        group_str = ",".join(group_by)
        type_str = child[0]
        where_str = " AND " + " AND ".join("%s='%s'" % (k,v) for k,v in sql_where)
    
    else:
        columns_str = "geo1, NULL, NULL, NULL"
        group_str = "geo1"
        type_str = 'geo1'
        where_str = ""
    
    if limit is not None:
      limit = "LIMIT %s" % limit
    else:
      limit = ""

    if sort == 'avg':
        sort_by = 'avg DESC'
    elif sort == 'recipients':
        sort_by = 'r DESC'
    elif sort == 'name':
        sort_by = '%s ASC' % type_str
    else:
        sort_by = 't DESC'

    cursor = connection.cursor()
    cursor.execute("""
    SELECT *, A.t/A.r as avg FROM
        (SELECT %(columns_str)s, country, MAX(recipients) as r, MAX(total) as t
        FROM data_locations
        WHERE country IN (%(countries)s) 
        AND location_type = '%(type_str)s'
        %(where_str)s
        GROUP BY %(group_str)s, country
        ORDER BY t DESC
        %(limit)s) as A
        ORDER BY %(sort_by)s
    """ % locals())

    result_list = []
    for row in cursor.fetchall():
      p = self.model()
      p.geo1=row[0]
      p.geo2=row[1]
      p.geo3=row[2]
      p.geo4=row[3]
      p.country=row[4]
      p.count=row[5]
      p.total=row[6]
      p.avg=row[7]
  
      p.name=p.__dict__.get(type_str, '')
  
      result_list.append(p)
    return result_list


  def recipients_by_location(self, country, geo1=None,geo2=None,geo3=None,geo4=None, limit=10, offset=0):
        if geo1:
          columns_available = [('geo1', geo1), ('geo2', geo2), ('geo3', geo3), ('geo4', geo4)]
          sql_columns = []
          sql_group = []
          sql_type = []
          sql_where = ""
          for k,v in columns_available:
              if v:
                  sql_columns.append(k)
                  sql_group.append(k)
                  sql_type.append(k)
                  sql_where += " AND LOWER(%s) = '%s'" % (k,v)
              else:
                  sql_columns.append('NULL')
          columns_str = ", ".join(sql_columns)
          group_str = ",".join(sql_group)
          type_str = sql_type[-1]
        else:
          columns_str = "geo1, NULL, NULL, NULL"
          group_str = "geo1"
          type_str = 'geo1'
          sql_where = "AND LOWER(geo1) IS NOT NULL"

        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM 
            (SELECT globalrecipientidx as global_id, name, geo1, geo2, geo3, geo4 FROM data_recipients
            WHERE countrypayment = '%(country)s'
            %(sql_where)s
            ) AS R
            JOIN data_totals T
            on R.global_id = T.global_id
            WHERE T.year='0'
            ORDER BY T.amount_euro DESC
            LIMIT %(limit)s
        """% locals())

        result_list = []
        for row in cursor.fetchall():
            p = self.model()
            p.global_id = row[0]
            p.name = row[1]
            p.geo1 = row[2]
            p.geo2 = row[3]
            p.geo3 = row[4]
            p.geo4 = row[5]
            p.amount_euro = row[7]
            p.global_id = row[0]
            result_list.append(p)
        return result_list




