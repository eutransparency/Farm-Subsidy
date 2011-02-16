from django.db import models

class Signee(models.Model):
    name = models.CharField(blank=False, max_length=255)
    affiliation = models.CharField(blank=True, max_length=255)
    email = models.EmailField(help_text='Will be kept private. See our <a href="/legal/">Privacy Policy</a>')
    comments = models.TextField(blank=True)


    def __unicode__(self):
        return self.name