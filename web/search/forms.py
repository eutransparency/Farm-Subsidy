from django import forms


class searchForm(forms.Form):
  q = forms.CharField(
      widget=forms.TextInput(attrs={'id':'q','title':'test'}),
      required=True, 
      label='Search', 
      help_text="""e.g. <a href="/search?q=nestle">Nestle</a> or <a href="/search?q=windsor">Windsor</a>"""
      )