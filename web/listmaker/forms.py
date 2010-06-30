import django.forms
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import List

class ListForm(forms.ModelForm):
    
    class Meta:
        model = List
        fields = ('name', 'description',)
