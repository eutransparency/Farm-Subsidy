from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
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
            return HttpResponseRedirect(reverse('home'))  
  
  return render_to_response('login.html', 
    {'login_form': login_form, 'registration_form': registration_form,}, 
    context_instance = RequestContext(request)
  )
  


def register(request):
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
          new_user = form.save()
          return HttpResponseRedirect("/")
  else:
      form = UserCreationForm()
  return render_to_response("user/register.html", {
      'form': form,
  })

  