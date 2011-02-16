from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

from forms import SigneeForm

def sign(request):
    
    form = SigneeForm()
    
    if request.POST:
        form = SigneeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sign_thanks'))
            
    
    return render_to_response(
        'sign.html', 
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

def sign_thanks(request):
    
    return render_to_response(
        'sign_thanks.html', 
        context_instance=RequestContext(request)
    )
