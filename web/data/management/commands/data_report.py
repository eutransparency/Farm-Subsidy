# -*- coding: utf-8 -*-
import StringIO
import codecs

import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models
from django.template.loader import render_to_string

from data import countryCodes
from data.models import Recipient


class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--output', '-o', dest='output',
        help='Full path to output file. Defaults to ./report.html'),
    )
    
    
    def handle(self, **options):
        
        page_content = StringIO.StringIO()
        
        for country in countryCodes.country_codes():
            print country
            template_data = {'country' : country}
            kwargs = {}
            if country != 'EU':
                kwargs['countrypayment'] = country
            template_data['top10'] = Recipient.objects.filter(**kwargs).order_by('-total')[:10]
            template_data['country_count'] = Recipient.objects.filter(**kwargs).count()
            page_content.write(render_to_string('datareport/country_section.html', template_data))

        page = render_to_string('datareport/base.html', {'page_content' : page_content.getvalue() })
        print type(page)
        output_path = options.get('output') or 'report.html'
        print output_path
        output_file = codecs.open(output_path, 'w', 'utf8')
        output_file.write(page)