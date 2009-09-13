from django.db import models
from managers import farmdata
# Create your models here.



class recipient(models.Model):
    recipientid = models.CharField(max_length=10)
    recipientidx = models.CharField(max_length=10)
    globalrecipientid = models.CharField(max_length=10,primary_key=True)
    globalrecipientidx = models.CharField(max_length=10)
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

class payment(models.Model):
    paymentid = models.IntegerField()
    globalpaymentid = models.CharField(max_length=10, primary_key=True)
    globalrecipientid = models.ForeignKey(recipient, db_column='globalrecipientid')
    globalrecipientidx = models.CharField(max_length=10)
    globalschemeid = models.CharField(max_length=10)
    amounteuro = models.TextField() # This field type is a guess.
    amountnationalcurrency = models.TextField() # This field type is a guess.
    year = models.IntegerField()
    countrypayment = models.CharField(max_length=2)
    class Meta:
        db_table = u'data_payments'


class scheme(models.Model):
    globalschemeid = models.CharField(max_length=-1, primary_key=True)
    namenationallanguage = models.TextField()
    nameenglish = models.TextField()
    budgetlines8digit = models.CharField(max_length=10)
    countrypayment = models.CharField(max_length=2)
    class Meta:
        db_table = u'data_schemes'

class total(models.Model):
    global_id = models.ForeignKey(recipient, db_column='globalrecipientidx')
    amount_euro = models.TextField() # This field type is a guess.
    year = models.IntegerField()
    countrypayment = models.CharField(max_length=2)
    class Meta:
        db_table = u'data_totals'

class data(models.Model):
  class Meta:
      abstract = True
  
  globalrecipientidx = models.TextField()
  name = models.TextField()
  amount_euro = models.TextField()
  year = models.TextField()
  
  
  
  objects = farmdata.FarmDataManager()


