import datetime
from haystack.indexes import *
from haystack import site
from data.models import Recipient, Location


class RecipientIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', default="unknown", weight=2)
    country = CharField(model_attr='countrypayment', default="unknown", faceted=True)
    
    def prepare_name(self, obj):
        obj._meta.module_name = "recipient"

site.register(Recipient, RecipientIndex)


class LocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', default="unknown", weight=2)
    country = CharField(model_attr='country', default="unknown", faceted=True)

site.register(Location, LocationIndex)
