from django import forms
from farmsubsidy.indexer import countryCodes
from django.template import Library, Node
register = Library()


class SearchForm(forms.Form):
  q = forms.CharField(label='Query')
  country = forms.ChoiceField(widget=forms.Select, choices=countryCodes.code2name)

