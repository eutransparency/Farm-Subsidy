import datetime
from haystack.indexes import *
from queued_search.indexes import QueuedSearchIndex
from haystack import site
from models import List


class ListIndex(QueuedSearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', weight=2)

site.register(List, ListIndex)
