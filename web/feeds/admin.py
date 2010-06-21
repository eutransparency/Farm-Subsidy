from django.contrib import admin
from web.feeds.models import *

class FeedsAdmin(admin.ModelAdmin):
  list_display  = ('title','url', 'is_active', 'category',)
  list_filter = ('category','is_active',)

class FeedItemsAdmin(admin.ModelAdmin):
  list_display  = ('title','url', 'tags','feed',)



admin.site.register(Feeds, FeedsAdmin)
admin.site.register(FeedItems, FeedItemsAdmin)
admin.site.register(FeedCategories)