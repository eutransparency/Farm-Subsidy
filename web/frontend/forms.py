import django.forms
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from models import Profile

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ('user', 'data_agreement', )


class DownloadDataForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name',)

class DataAgreementForm(forms.ModelForm):
    
    data_agreement = forms.BooleanField(required=True, label=_('I Agree to the terms above'))
    data_description = forms.CharField(required=True, label=_('Tell us something about what you plan to do with the data'), widget=forms.Textarea)
    
    class Meta:
        model = Profile
        fields = ('data_agreement', 'data_description',)
