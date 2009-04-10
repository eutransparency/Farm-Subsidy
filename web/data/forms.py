from django import forms
from farmsubsidy.indexer import countryCodes
from django.template import Library, Node
register = Library()


class SearchForm(forms.Form):
  
  choices = []
  for code,name in countryCodes.code2name.items():
    choices.append((code,name))
  
  q = forms.CharField(label='Search', help_text='e.g. Nestle or Guildiford, UK or France')
  country = forms.ChoiceField(widget=forms.Select, choices=choices)


class SearchFormLite(forms.Form):
  q = forms.CharField(label='', help_text='e.g. <a href="/search?q=nestle">Nestle</a> or <a href="/search?q=guildford">Guildford</a>, <a href="search?q=country:UK">UK</a> or <a href="/search?q=country:FR">France</a>')

