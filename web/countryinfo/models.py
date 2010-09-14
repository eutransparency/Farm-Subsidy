from django.db import models


class TransparencyScore(models.Model):
    country = models.CharField(blank=False, max_length=2, primary_key=True)
    score = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)