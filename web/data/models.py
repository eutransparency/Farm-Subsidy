from django.db import models
from managers import farmdata
# Create your models here.



class recipient(models.Model):
    recipientid = models.CharField(max_length=10)
    recipientidx = models.CharField(max_length=10)
    globalrecipientid = models.CharField(max_length=10)
    globalrecipientidx = models.CharField(max_length=10,primary_key=True)
    name = models.TextField()
    address1 = models.TextField()
    address2 = models.TextField()
    zipcode = models.CharField(max_length=10)
    town = models.TextField()
    countryrecipient = models.CharField(max_length=2)
    countrypayment = models.CharField(max_length=2)
    geo1 = models.TextField()
    geo2 = models.TextField()
    geo3 = models.TextField()
    geo4 = models.TextField()
    geo1nationallanguage = models.TextField()
    geo2nationallanguage = models.TextField()
    geo3nationallanguage = models.TextField()
    geo4nationallanguage = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    class Meta:
        db_table = u'data_recipients'
    
    def __unicode__(self):
      return "%s (%s)" % (self.globalrecipientidx, self.name)

class payment(models.Model):
    paymentid = models.IntegerField()
    globalpaymentid = models.CharField(max_length=10, primary_key=True)
    globalrecipientid = models.ForeignKey(recipient, db_column='globalrecipientid')
    globalrecipientidx = models.CharField(max_length=10)
    globalschemeid = models.ForeignKey('scheme', db_column='globalschemeid')
    amounteuro = models.TextField() # This field type is a guess.
    amountnationalcurrency = models.TextField() # This field type is a guess.
    year = models.IntegerField()
    countrypayment = models.CharField(max_length=2)
    class Meta:
        db_table = u'data_payments'
        

class scheme(models.Model):
    globalschemeid = models.CharField(max_length=40, primary_key=True)
    namenationallanguage = models.TextField()
    nameenglish = models.TextField()
    budgetlines8digit = models.CharField(max_length=10)
    countrypayment = models.CharField(max_length=2)
    class Meta:
        db_table = u'data_schemes'

class total(models.Model):
    global_id = models.CharField(max_length=40, primary_key=True)
    amount_euro = models.TextField() # This field type is a guess.
    year = models.IntegerField()
    countrypayment = models.CharField(max_length=2)
    nameenglish = models.TextField()    
    class Meta:
        db_table = u'data_totals'

class counts(models.Model):
    country = models.CharField(blank=True, max_length=100)
    year = models.IntegerField()
    type = models.CharField(max_length=40)
    value = models.CharField(blank=True, max_length=100, primary_key=True)
    count = models.IntegerField()
    
    class Meta:
        db_table = u'data_counts'


class locations(models.Model):
    country = models.CharField(max_length=2)
    year = models.IntegerField()
    name = models.TextField(primary_key=True)    
    parent_name = models.TextField()    
    total = models.TextField() # This field type is a guess.

    objects = farmdata.LocationManager()
    
    class Meta:
        db_table = u'data_locations'
        managed = False

    def __unicode__(self):
      return "%s (%s)" % (self.name, self.parent_name)
    

class data(models.Model):
  class Meta:
      abstract = True
  
  globalrecipientidx = models.TextField()
  name = models.TextField()
  amount_euro = models.TextField()
  year = models.TextField()
  globalschemeid = models.TextField()
  country = models.TextField()
  
  
  
  objects = farmdata.FarmDataManager()


