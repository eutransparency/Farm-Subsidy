from django import forms
from django import forms
from haystack.forms import SearchForm


class SearchForm(SearchForm):
    q = forms.CharField(
        widget=forms.TextInput(attrs={'id':'q','title':'Enter a company name or place'}),
        required=True, 
        label='Search', 
        help_text="""e.g. <a href="/search/nestle">Nestle</a> or <a href="/search/windsor">Windsor</a>"""
        )

