from django import forms

class ContactForm(forms.Form):
  subject = forms.CharField()
  email = forms.EmailField(required=False, label='Your e-mail address')
  message = forms.CharField()
    