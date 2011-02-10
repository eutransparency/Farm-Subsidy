import django.forms
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Signee

class SigneeForm(forms.ModelForm):
    
    class Meta:
        model = Signee
