from django.contrib import admin
from farmjango.api.models import blog

class blogAdmin(admin.ModelAdmin):
  list_display = ('title', 'published')
  # search_fields = ('title', 'body')
  list_filter = ('published',)


admin.site.register(blog, blogAdmin)

