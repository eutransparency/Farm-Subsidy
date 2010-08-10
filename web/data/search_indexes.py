import datetime
from haystack.indexes import *
from haystack import site
from data.models import Recipient


class RecipientIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', default="unknown", weight=2)
    #scheme = MultiValueField(faceted=True)
    country = CharField(model_attr='countrypayment', default="unknown", faceted=True)

#    def prepare_scheme(self, obj):
#            # Since we're using a M2M relationship with a complex lookup,
#            # we can prepare the list here.
#            scheme_names = set()
#            for p in obj.payment_set.all():
#                try:
#                    scheme_names.add(p.scheme.nameenglish)
#                except:
#                    pass
#            return list(scheme_names)

site.register(Recipient, RecipientIndex)
