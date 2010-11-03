"""
Various bits to clean upthe data.

This code is horrid.  I mean really horrid.

And it does something specific, so edit with care, and test!

"""
from optparse import make_option

import django
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models
import treebeard

from data.models import Recipient, Location


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
        help='ISO country name'),
    )
    help = 'Normalizeation scripts for the farm data'
    
    def dictfetchall(self, cursor, geo1=False): 
        "Returns all rows from a cursor as a dict" 
        desc = cursor.description
        d = {}
        for r in cursor.fetchall():
            if not d.get(r[0]):
                d[r[0]] = {}
            if geo1:
                d[r[0]]["%s" % (r[1])] = dict(zip([col[0] for col in desc], r))
            else:
                d[r[0]]["%s:%s" % (r[1], r[2])] = dict(zip([col[0] for col in desc], r))
        return d
        
        # return [dict(zip([col[0] for col in desc], row))   for row in cursor.fetchall()]
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        
        # # Make all locations lower case by default
        # print "Lowering location names"
        # cursor = connection.cursor()
        # cursor.execute("""
        # UPDATE data_recipient 
        # SET geo1=lower(geo1), geo2=lower(geo2), geo3=lower(geo3), geo4=lower(geo4)
        # WHERE countrypayment='%(country)s';
        # """ % {'country' : self.country})
        
        Location.objects.filter(country=self.country).delete()
        
        # Geo1 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo1, p.year, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            JOIN data_payment p
            ON r.globalrecipientidx=p.globalrecipientidx
            WHERE r.countrypayment='%(country)s'
            AND p.countrypayment='%(country)s'
            AND r.geo1 IS NOT NULL
            GROUP BY r.geo1, p.year;
        """ % {'country' : self.country})
        geo1_total = self.dictfetchall(cursor, geo1=True)

        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo1, '0' as year, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            WHERE r.countrypayment='%(country)s'
            AND r.geo1 IS NOT NULL
            GROUP BY r.geo1;
        """ % {'country' : self.country})
        geo1_total_all = self.dictfetchall(cursor, geo1=True)
        for k,v in geo1_total.items():
            v['0'] = geo1_total_all[k]['0']
        
        # Geo2 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo2, p.year, r.geo1, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            JOIN data_payment p
            ON r.globalrecipientidx=p.globalrecipientidx
            WHERE r.countrypayment='%(country)s'
            AND p.countrypayment='%(country)s'
            AND r.geo2 IS NOT NULL
            GROUP BY r.geo1, r.geo2, p.year
        """ % {'country' : self.country})
        geo2_total = self.dictfetchall(cursor)
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo2, '0' as year, r.geo1, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            WHERE r.countrypayment='%(country)s'
            AND r.geo2 IS NOT NULL
            GROUP BY r.geo1, r.geo2;
        """ % {'country' : self.country})
        geo2_total_all = self.dictfetchall(cursor)

        for k,v in geo2_total_all.items():
            geo2_total[k].update(v)

                
        # Geo3 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo3, p.year, r.geo2, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            JOIN data_payment p
            ON r.globalrecipientidx=p.globalrecipientidx
            WHERE r.countrypayment='%(country)s'
            AND p.countrypayment='%(country)s'
            AND r.geo3 IS NOT NULL
            GROUP BY r.geo1, r.geo2, r.geo3, p.year
        """ % {'country' : self.country})
        geo3_total = self.dictfetchall(cursor)

        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo3, '0' as year, r.geo2, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            WHERE r.countrypayment='%(country)s'
            AND r.geo3 IS NOT NULL
            GROUP BY r.geo1, r.geo2, r.geo3;
        """ % {'country' : self.country})
        geo3_total_all = self.dictfetchall(cursor)
        for k,v in geo3_total_all.items():
            geo3_total[k].update(v)
        


        # Geo4 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo4, p.year, r.geo3, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            JOIN data_payment p
            ON r.globalrecipientidx=p.globalrecipientidx
            WHERE r.countrypayment='%(country)s'
            AND p.countrypayment='%(country)s'
            AND r.geo4 IS NOT NULL
            GROUP BY r.geo1, r.geo2, r.geo3, r.geo4, p.year
        """ % {'country' : self.country})
        geo4_total = self.dictfetchall(cursor)

        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.geo4, '0' as year, r.geo3, SUM(r.total) as total, COUNT(r.*) as count, AVG(r.lat) as lat, AVG(r.lng) as lng
            FROM data_recipient r
            WHERE r.countrypayment='%(country)s'
            AND r.geo4 IS NOT NULL
            GROUP BY r.geo1, r.geo2, r.geo3, r.geo4;
        """ % {'country' : self.country})
        geo4_total_all = self.dictfetchall(cursor)
        for k,v in geo4_total_all.items():
            geo4_total[k].update(v)
        


        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo1, geo2, geo3, geo4
            FROM data_recipient
            WHERE countrypayment='%s'
            AND geo1 IS NOT NULL
            GROUP BY geo1, geo2, geo3, geo4
            ORDER BY geo1, geo2, geo3, geo4
        """ % self.country)
        
        geo1 = geo2 = geo3 = geo4 = None
        geo1_obj = geo2_obj = geo3_obj = geo4_obj = {}
        data = {}
        
        def make_slug(parent, name):
            path_list = [o.name for o in parent.get_ancestors()]
            path_list.append(name)
            slug = "/".join([slugify(n) for n in path_list])
            return slug
            
        
        for location in cursor.fetchall():
        
            if geo1 != location[0]:
                geo1 = location[0]
                geo2 = geo3 = geo4 = None
                geo1_obj = {}
                if geo1 != "":
                    for year, location_year in geo1_total[geo1].items():
                        if not geo1_obj.get(location_year['geo1']):
                            geo1_obj[location_year['geo1']] = {}
                        geo1_obj[location_year['geo1']].update({year : {}})
                        geo1_obj[location_year['geo1']][year] = Location().add_root(geo_type='geo1', 
                                        name=geo1, 
                                        country=self.country,
                                        slug=make_slug(Location(), geo1),
                                        total=location_year['total'],
                                        recipients=location_year['count'],
                                        average=location_year['total']/location_year['count'],
                                        lat=location_year['lat'],
                                        lon=location_year['lng'],
                                        year=year,
                                        )
            if geo2 != location[1]:
                
                 geo2 = location[1]
                 geo3 = geo4 = None
                 geo2_obj = {}
                 if geo2 != "" and geo2 is not None:
                     for year, location_year in geo2_total[geo2].items():
                         (year, parent) = year.split(':')
                         if not geo2_obj.get(location_year['geo2']):
                             geo2_obj[location_year['geo2']] = {}
                         if location_year['geo1'] == geo1:
                         
                             geo2_obj[location_year['geo2']].update({year : {}})
                             geo2_obj[location_year['geo2']][year] = geo1_obj[location[0]][year].add_child(geo_type='geo2',
                                            name=geo2, 
                                            country=self.country,
                                            total=location_year['total'],
                                            recipients=location_year['count'],
                                            average=location_year['total']/location_year['count'],
                                            lat=location_year['lat'],
                                            lon=location_year['lng'],
                                            year=year
                                            )
                             geo2_obj[location_year['geo2']][year].slug=make_slug(geo2_obj[location_year['geo2']][year], geo2)
                             geo2_obj[location_year['geo2']][year].save()
            

            if geo3 != location[2]:
                geo3 = location[2]
                geo4 = None
                geo3_obj = {}
                if geo2 != "" and geo3 != "" and geo3 is not None:
                    for year, location_year in geo3_total[geo3].items():
                        (year, parent) = year.split(':')
                        if not geo3_obj.get(location_year['geo3']):
                            geo3_obj[location_year['geo3']] = {}
                        if location_year['geo2'] == geo2:
                            geo3_obj[location_year['geo3']].update({year : {}})
                            geo3_obj[location_year['geo3']][year] = geo2_obj[location[1]][year].add_child(geo_type='geo3',
                                            name=geo3, 
                                            country=self.country,
                                            total=location_year['total'], 
                                            recipients=location_year['count'],
                                            average=location_year['total']/location_year['count'],
                                            lat=location_year['lat'],
                                            lon=location_year['lng'],
                                            year=year,
                                            )
                            geo3_obj[location_year['geo3']][year].slug=make_slug(geo3_obj[location_year['geo3']][year], geo3)
                            geo3_obj[location_year['geo3']][year].save()
                
            if geo4 != location[3]:
                geo4 = location[3]
                geo4_obj = {}
                if geo2 != "" and geo3 != "" and geo4 != "" and geo4 is not None:
                    for year, location_year in geo4_total[geo4].items():
                        (year, parent) = year.split(':')
                        if not geo4_obj.get(location_year['geo4']):
                            geo4_obj[location_year['geo4']] = {}
                        if location_year['geo3'] == geo3:
                            geo4_obj[location_year['geo4']].update({year : {}})
                            geo4_obj[location_year['geo4']][year] = geo3_obj[location[2]][year].add_child(geo_type='geo4',
                                            name=geo4, 
                                            country=self.country,
                                            total=location_year['total'], 
                                            recipients=location_year['count'],
                                            average=location_year['total']/location_year['count'],
                                            lat=location_year['lat'],
                                            lon=location_year['lng'],
                                            year=year,
                                            )
                            geo4_obj[location_year['geo4']][year].slug=make_slug(geo4_obj[location_year['geo4']][year], geo4)
                            geo4_obj[location_year['geo4']][year].save()
                
            # if geo4 != location[3]:
            #     geo4 = location[3]
            #     if geo2 != "" and geo3 != "" and geo4 != "" and geo4 is not None:
            #         for year, location_year in geo4_total[geo4].items():
            #             geo4_obj[year] = geo3_obj[year].add_child(geo_type='geo4',
            #                             name=geo4, 
            #                             country=self.country,
            #                             slug=make_slug(geo3_obj, geo4),
            #                             total=location_year['total'],
            #                             recipients=location_year['count'],
            #                             average=location_year['total']/location_year['count'],
            #                             lat=location_year['lat'],
            #                             lon=location_year['lng'],
            #                             year=year,
            #                             )
            #             geo4_obj[year].slug=make_slug(geo4_obj[year], geo4)
            #             geo4_obj[year].save()
            # 
