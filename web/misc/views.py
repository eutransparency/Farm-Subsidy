from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib import auth
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def login(request):
  login_form = AuthenticationForm()
  registration_form = RegistrationForm()
  
  if request.POST:
    
    login_form = AuthenticationForm(request.POST)
    registration_form = RegistrationForm(request.POST)
    
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('home'))  
    if registration_form.is_valid():
        new_user = registration_form.save()
        return HttpResponseRedirect(reverse('registration_complete'))
  
  return render_to_response('login.html', 
    {
        'login_form': login_form, 
        'registration_form': registration_form,
        'next' : request.GET.get('next', '/'),
    }, 
    context_instance = RequestContext(request)
  )