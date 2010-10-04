import datetime
from haystack.indexes import *
from queued_search.indexes import QueuedSearchIndex
from haystack import site
from features.models import Feature


class FeatureIndex(QueuedSearchIndex):
    text = CharField(document=True, use_template=True)
    published = BooleanField(model_attr='published', default=False)

    def get_queryset(self):
            """Used when the entire index for model is updated."""
            return Feature.objects.filter(published=True)

site.register(Feature, FeatureIndex)
