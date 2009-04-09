from django import forms
from farmsubsidy.indexer import countryCodes
from django.template import Library, Node
register = Library()


class SearchForm(forms.Form):
  
  choices = []
  for code,name in countryCodes.code2name.items():
    choices.append((code,name))
  
  q = forms.CharField(label='Search')
  country = forms.ChoiceField(widget=forms.Select, choices=choices)


class SearchFormLite(forms.Form):
  q = forms.CharField(label='')

