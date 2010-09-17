import datetime
from haystack.indexes import *
from haystack import site
from features.models import Feature


class FeatureIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Feature, FeatureIndex)
