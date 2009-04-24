from django import forms

class CommentForm(forms.Form):
  comment = forms.CharField(widget=forms.Textarea)
  owner = forms.BooleanField(required=False, label="Are you the recipient?")
