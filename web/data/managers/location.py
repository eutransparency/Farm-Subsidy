# encoding: utf-8
import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max

from data import countryCodes
import fsconf

DEFAULT_YEAR = fsconf.default_year

class LocationManager(models.Manager):
    pass