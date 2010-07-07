from django.db import models
from django.core.cache import cache
from django.core.urlresolvers import reverse

class Feature(models.Model):
    """
    For displaying featured items, like reports or news items.
    """
    
    def __unicode__(self):
        return self.title
    
    def save(self, commit=False, message=None, user=None):        
        super(Feature, self).save()

        # After save, clear the cached items
        cache.delete('featured_items')

    title = models.CharField(blank=False, max_length=255)
    slug = models.SlugField(help_text="Forms the URL of the feature, no spaces or fancy characters. best to separate words with hyphens")
    teaser = models.TextField(blank=True, help_text="Appers are the top of every page, shortened to about 25 words")
    body = models.TextField(blank=True)        
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('feature_detail', args=[self.slug,])
    
    
    # class Translation(multilingual.Translation):
    #     title = models.CharField(blank=False, max_length=255)
    #     slug = models.SlugField(help_text="Forms the URL of the feature, no spaces or fancy characters. best to separate words with hyphens")
    #     teaser = models.TextField(blank=True, help_text="Appers are the top of every page, shortened to about 25 words")
    #     body = models.TextField(blank=True)
    