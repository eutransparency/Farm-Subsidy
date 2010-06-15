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
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        Location.objects.filter(country=self.country).delete()
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo1, geo2, geo3, geo4
            FROM data_recipient
            GROUP BY geo1, geo2, geo3, geo4
            ORDER BY geo1, geo2, geo3, geo4
        """)
        
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
                    print geo1
                    geo1_obj = Location().add_root(geo_type='geo1', 
                                    name=geo1, 
                                    country=self.country,
                                    slug=make_slug(Location(), geo1),
                                    total=0, 
                                    average=0)

            if geo2 != location[1]:
                 geo2 = location[1]
                 if geo2 != "":
                     print "\t %s" % geo2
                     geo2_obj = geo1_obj.add_child(geo_type='geo2',
                                    name=geo2, 
                                    country=self.country,
                                    total=0,
                                    average=0)
                     geo2_obj.slug=make_slug(geo2_obj, geo2)
                     geo2_obj.save()

            if geo3 != location[2]:
                geo3 = location[2]
                if geo2 != "" and geo3 != "":
                    print "\t\t %s" % geo3
                    geo3_obj = geo2_obj.add_child(geo_type='geo3',
                                    name=geo3, 
                                    country=self.country,
                                    slug=make_slug(geo2_obj, geo3),
                                    total=0,
                                    average=0)
                    geo3_obj.slug=make_slug(geo3_obj, geo3)
                    geo3_obj.save()
                    
            if geo4 != location[3]:
                geo4 = location[3]
                if geo2 != "" and geo3 != "" and geo4 != "":
                    print "\t\t\t %s" % geo4
                    geo4_obj = geo3_obj.add_child(geo_type='geo4',
                                    name=geo4, 
                                    country=self.country,
                                    slug=make_slug(geo3_obj, geo4),
                                    total=0,
                                    average=0)
                    geo4_obj.slug=make_slug(geo4_obj, geo4)
                    geo4_obj.save()
                    
                    

