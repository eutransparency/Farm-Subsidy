from django.contrib.syndication.views import Feed
from models import Feature

class FeaturesFeed(Feed):
    title = "Farmsubsidy.org"
    link = "/news/"
    description = "News about Farmsubsidy.org"

    def items(self):
        return Feature.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser