# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from treebeard.mp_tree import MP_Node
from django.contrib.gis.db import models as geo_models

from managers.recipients import RecipientManager
from managers.schemes import SchemeManager, SchemeYearManager
from managers.countryyear import CountryYearManager

import countryCodes

class CountryYear(models.Model):
    year = models.IntegerField(blank=True, null=True)
    country = models.CharField(blank=True, max_length=2)
    total = models.FloatField()
    
    class Meta:
        get_latest_by = 'year'
        ordering = ( 'year', )
    
    
    objects = CountryYearManager()


class Recipient(models.Model):
    recipientid = models.CharField(max_length=10)
    recipientidx = models.CharField(max_length=10)
    globalrecipientid = models.CharField(max_length=10)
    globalrecipientidx = models.CharField(max_length=10,primary_key=True)
    name = models.TextField(null=True)
    address1 = models.TextField(null=True)
    address2 = models.TextField(null=True)
    zipcode = models.CharField(max_length=20, null=True)
    town = models.TextField(null=True)
    countryrecipient = models.CharField(max_length=2, null=True, db_index=True)
    countrypayment = models.CharField(max_length=2, null=True, db_index=True)
    geo1 = models.TextField(null=True)
    geo2 = models.TextField(null=True)
    geo3 = models.TextField(null=True)
    geo4 = models.TextField(null=True)
    geo1nationallanguage = models.TextField(null=True)
    geo2nationallanguage = models.TextField(null=True)
    geo3nationallanguage = models.TextField(null=True)
    geo4nationallanguage = models.TextField(null=True)
    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)
    total = models.FloatField(null=True, db_index=True)

    objects = RecipientManager()

    LIST_ENABLED = True
    list_hash_fields = ('name', 'countrypayment', 'total')
    list_total_field = 'total'
    

    def __unicode__(self):
        return "%s (%s)" % (self.pk, self.name)
    
    class Meta():
        ordering = ('-total',)
    
    def get_absolute_url(self):
        return reverse('recipient_view', args=[self.countrypayment, self.pk, slugify(self.name)])
    
    def geo_url(self, geo_type):
        """
        Returns a URL (from reverse()) for a location.
        """

        geos = [self.geo1,self.geo2,self.geo3,self.geo4,]
        slug = "/".join([slugify(n) for n in geos[:geo_type]])
        return reverse('location_view', args=[self.countrypayment, 0, slug])
    
    def geo1_url(self):
        return self.geo_url(1)

    def geo2_url(self):
        return self.geo_url(2)

    def geo3_url(self):
        return self.geo_url(3)

    def geo4_url(self):
        return self.geo_url(4)


class GeoRecipient(geo_models.Model):
    recipient = models.ForeignKey(Recipient, primary_key=True)
    location = geo_models.PointField()

    objects = geo_models.GeoManager()

    def __unicode__(self):
        return self.pk


class Payment(models.Model):
    paymentid = models.TextField()
    globalpaymentid = models.CharField(max_length=10, primary_key=True)
    globalrecipientid = models.TextField()
    recipient = models.ForeignKey(
                                Recipient, 
                                db_column='globalrecipientidx', 
                                max_length=10,
                                db_index=True,
                                )
    scheme = models.ForeignKey('Scheme', db_column='globalschemeid')
    amounteuro = models.FloatField(null=True, db_index=True) # This field type is a guess.
    amountnationalcurrency = models.FloatField(null=True) # This field type is a guess.
    year = models.IntegerField(db_index=True)
    countrypayment = models.CharField(max_length=4, default=None, db_index=True)

    # class Meta():
    #     managed = False


class Scheme(models.Model):
    globalschemeid = models.CharField(max_length=40, primary_key=True)
    namenationallanguage = models.TextField(null=True)
    nameenglish = models.TextField(db_index=True)
    budgetlines8digit = models.CharField(max_length=10, null=True)
    countrypayment = models.CharField(max_length=2)
    total = models.FloatField()
    
    objects = SchemeManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.pk, self.nameenglish)
    
    def get_absolute_url(self):
        return reverse('scheme_view', args=[self.countrypayment, 
                                            self.pk, 
                                            slugify(self.nameenglish)])


class SchemeYear(models.Model):
    globalschemeid = models.CharField(blank=True, max_length=40, db_index=True)
    nameenglish = models.TextField(blank=True)
    countrypayment = models.CharField(blank=True, max_length=2)
    year = models.IntegerField(blank=True, null=True)
    total = models.FloatField()

    objects = SchemeYearManager()

    def get_absolute_url(self):
        return reverse('scheme_view', args=[self.countrypayment, 
                                            self.globalschemeid, 
                                            slugify(self.nameenglish)])



class SchemeType(models.Model):
    """
    Model for defining what broad category a scheme fits in to.
    
    See the "scheme_types" managment command for how this is populated.
    """
    DIRECT = 0
    INDIRECT = 1
    RURAL = 2
    
    SCHEME_TYPES = (
        (DIRECT, 'Direct'),
        (INDIRECT, 'Indirect'),
        (RURAL, 'Rural'),
    )
    
    globalschemeid = models.ForeignKey(Scheme, primary_key=True)
    country = models.CharField(blank=False, max_length=2, choices=((i,i) for i in countryCodes.country_codes()))
    scheme_type = models.IntegerField(choices=SCHEME_TYPES)

    def __unicode__(self):
        return "%s - %s" % (self.globalschemeid, self.scheme_type)

class TotalYear(models.Model):
    recipient = models.ForeignKey(Recipient, db_index=True)
    year = models.IntegerField(blank=True, null=True, db_index=True)
    total = models.FloatField(db_index=True)
    country = models.CharField(blank=False, max_length=2)


class Location(MP_Node):

    geo_type = models.CharField(blank=True, max_length=10)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.CharField(blank=True, max_length=100)
    recipients = models.IntegerField(blank=True, null=True)
    total = models.FloatField()
    average = models.FloatField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    year = models.IntegerField(blank=True, null=True, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_view', args=[self.country, self.year, self.slug])
    
class DataDownload(models.Model):

    public = models.BooleanField(default=True)
    filename = models.CharField(blank=True, max_length=255)
    format = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    file_path = models.CharField(blank=True, max_length=255)
    download_count = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.filename
