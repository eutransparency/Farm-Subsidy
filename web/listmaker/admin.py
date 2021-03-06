from django.contrib import admin

from models import *


class ListInlines(admin.TabularInline):
  model = ListItem
  # extra = 1

class ListAdmin(admin.ModelAdmin):
    inlines = (ListInlines,)
    list_display = ('name','user',)
    prepopulated_fields = {"slug": ("name",)}



admin.site.register(List, ListAdmin)
admin.site.register(ListItem)
