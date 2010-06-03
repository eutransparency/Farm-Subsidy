from django.contrib import admin
from models import Recipient
# 
# # class FeedsAdmin(admin.ModelAdmin):
# #   list_display  = ('title','url', 'is_active', 'category',)
# #   list_filter = ('category','is_active',)
# # 
# # class FeedItemsAdmin(admin.ModelAdmin):
# #   list_display  = ('title','url', 'tags','feed',)
# 
# from treebeard.admin import TreeAdmin
# 
# class LocationAdmin(TreeAdmin):
#     prepopulated_fields = {"slug": ("name",)}
# 
admin.site.register(Recipient)
# # admin.site.register(FeedItems, FeedItemsAdmin)
# # admin.site.register(FeedCategories)