"""
Various bits to clean upthe data

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
    
    def dictfetchall(self, cursor): 
        "Returns all rows from a cursor as a dict" 
        desc = cursor.description
        d = {}
        for r in cursor.fetchall():
            d[r[0]] = dict(zip([col[0] for col in desc], r))
        return d
        
        # return [dict(zip([col[0] for col in desc], row))   for row in cursor.fetchall()]
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        Location.objects.filter(country=self.country).delete()
        
        # Geo1 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo1, SUM(total) as total, COUNT(*) as count, MAX(lat) as lat, MAX(lng) as lng
            FROM data_recipient
            WHERE countrypayment='%s'
            AND geo1 IS NOT NULL
            GROUP BY geo1
        """ % self.country)
        geo1_total = self.dictfetchall(cursor)

        
        # Geo2 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo2, SUM(total) as total, COUNT(*) as count, MAX(lat) as lat, MAX(lng) as lng
            FROM data_recipient
            WHERE countrypayment='%s'
            AND geo2 IS NOT NULL
            GROUP BY geo1, geo2
        """ % self.country)
        geo2_total = self.dictfetchall(cursor)

        # Geo3 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo3, SUM(total) as total, COUNT(*) as count, MAX(lat) as lat, MAX(lng) as lng
            FROM data_recipient
            WHERE countrypayment='%s'
            AND geo3 IS NOT NULL
            GROUP BY geo1, geo2, geo3
        """ % self.country)
        geo3_total = self.dictfetchall(cursor)
        
        # Geo4 totals
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo4, SUM(total) as total, COUNT(*) as count, MAX(lat) as lat, MAX(lng) as lng
            FROM data_recipient
            WHERE countrypayment='%s'
            AND geo4 IS NOT NULL
            GROUP BY geo1, geo2, geo3, geo4
        """ % self.country)
        geo4_total = self.dictfetchall(cursor)

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
        data = {}
        
        def make_slug(parent, name):
            path_list = [o.name for o in parent.get_ancestors()]
            path_list.append(name)
            slug = "/".join([slugify(n) for n in path_list])
            return slug
            
        
        for location in cursor.fetchall():
            if geo1 != location[0]:
                geo1 = location[0]
                if geo1 != "":
                    geo1_obj = Location().add_root(geo_type='geo1', 
                                    name=geo1, 
                                    country=self.country,
                                    slug=make_slug(Location(), geo1),
                                    total=geo1_total[geo1]['total'],
                                    recipients=geo1_total[geo1]['count'],
                                    average=geo1_total[geo1]['total']/geo1_total[geo1]['count'],
                                    lat=geo1_total[geo1]['lat'],
                                    lon=geo1_total[geo1]['lng'],
                                    )

            if geo2 != location[1]:
                 geo2 = location[1]
                 if geo2 != "" and geo2 is not None:
                     geo2_obj = geo1_obj.add_child(geo_type='geo2',
                                    name=geo2, 
                                    country=self.country,
                                    total=geo2_total[geo2]['total'],
                                    recipients=geo2_total[geo2]['count'],
                                    average=geo2_total[geo2]['total']/geo2_total[geo2]['count'],
                                    lat=geo2_total[geo2]['lat'],
                                    lon=geo2_total[geo2]['lng'],
                                    )
                     geo2_obj.slug=make_slug(geo2_obj, geo2)
                     geo2_obj.save()

            if geo3 != location[2]:
                geo3 = location[2]
                if geo2 != "" and geo3 != "" and geo3 is not None:
                    geo3_obj = geo2_obj.add_child(geo_type='geo3',
                                    name=geo3, 
                                    country=self.country,
                                    slug=make_slug(geo2_obj, geo3),
                                    total=geo3_total[geo3]['total'], 
                                    recipients=geo3_total[geo3]['count'],
                                    average=geo3_total[geo3]['total']/geo3_total[geo3]['count'],
                                    lat=geo3_total[geo3]['lat'],
                                    lon=geo3_total[geo3]['lng'],
                                    )
                    geo3_obj.slug=make_slug(geo3_obj, geo3)
                    geo3_obj.save()
                    
            if geo4 != location[3]:
                geo4 = location[3]
                if geo2 != "" and geo3 != "" and geo4 != "" and geo4 is not None:
                    geo4_obj = geo3_obj.add_child(geo_type='geo4',
                                    name=geo4, 
                                    country=self.country,
                                    slug=make_slug(geo3_obj, geo4),
                                    total=geo4_total[geo4]['total'],
                                    recipients=geo4_total[geo4]['count'],
                                    average=geo4_total[geo4]['total']/geo4_total[geo4]['count'],
                                    lat=geo4_total[geo4]['lat'],
                                    lon=geo4_total[geo4]['lng'],
                                    )
                    geo4_obj.slug=make_slug(geo4_obj, geo4)
                    geo4_obj.save()
                    
                    

