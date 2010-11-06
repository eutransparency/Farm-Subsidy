# -*- coding: utf-8 -*-
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from registration.forms import RegistrationForm
from django.contrib.auth.forms import User
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from models import Profile
from forms import ProfileForm

def robots(request):
    res = HttpResponse()
    res.write(
"""User-agent: *
Crawl-delay: 5
""")
    return res


def login(request):
    #grab the redirect URL if set
    if request.POST.get('next'):
        redirect = request.POST.get('next')
    elif request.POST.get('redirect'):
        redirect = request.POST.get('redirect')
    elif request.GET.get('next'):
        redirect = request.GET.get('next')
    else:
        redirect = request.META.get('HTTP_REFERER', '/')
        if redirect.endswith("login"):
            redirect = "/myaccount"
    
    
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
                return HttpResponseRedirect(redirect)
        if registration_form.is_valid():
            u = User(username=request.POST['username'],
                                    email=request.POST['email'],
                                     )
            u.set_password(request.POST['password1'])
            u.is_active = True
            u.save()
            p = Profile(user=u)
            p.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])

            auth.login(request, user)
            return HttpResponseRedirect(redirect)
  
    return render_to_response('login.html', 
    {
        'login_form': login_form, 
        'registration_form': registration_form,
        'redirect' : redirect,
    }, 
    context_instance = RequestContext(request)
    )

def logout(request):
    user = request.user
    if request.POST.get('logout'):
        auth.logout(request)
        return HttpResponseRedirect('/')

    return render_to_response('logout.html', 
    {}, 
    context_instance = RequestContext(request)
    )
    
    

@login_required
def dashboard(request):
    user = request.user
    latest_annotations = user.comment_comments.all()[:5]
    latest_lists = user.list_set.all()[:5]
    
    return render_to_response('dashboard.html', 
    {
        'user' : user,
        'latest_annotations' : latest_annotations,
        'latest_lists' : latest_lists,
    }, 
    context_instance = RequestContext(request)
    )


@login_required
def annotations(request):
    user = request.user
    annotations = user.comment_comments.all()
    
    return render_to_response('annotations.html', 
    {
        'user' : user,
        'annotations' : annotations,
    }, 
    context_instance = RequestContext(request)
    )

@login_required
def lists(request):
    user = request.user
    lists = user.list_set.all()
    
    return render_to_response('lists.html', 
    {
        'user' : user,
        'lists' : lists,
    }, 
    context_instance = RequestContext(request)
    )

@login_required
def account(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Exception, e:
        print e
        profile = Profile(user=user)
        profile.save()

    form = ProfileForm(instance=profile)
    
    return render_to_response('account.html', 
    {
        'user' : user,
        'profile' : profile,
        'form' : form,
    }, 
    context_instance = RequestContext(request)
    )



def server_error(request, template_name='500.html'):
    """
    Override the default 500 error view to add settings.MEDIA_URL.
    """
    from django import http
    from django.template import Context, RequestContext, loader
    
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(
        Context({
            'MEDIA_URL' : settings.MEDIA_URL
        })
        ))
