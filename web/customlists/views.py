import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from farmsubsidy.queries import queries
import cPickle

def main(request):
  if request.method == "POST":
    request.session['create_list'] = True
    request.session['list_items'] = {}
    return HttpResponseRedirect(
      reverse("main_list_view")
      )
  
  # del request.session['list_items']
  # del request.session['create_list']
  
  return render_to_response('main.html',
    context_instance=RequestContext(request)
  )
  
def add_to_list(request):
  if request.method == "POST":
    list_items = request.session['list_items']
    for key,docid in request.POST.items():
      if key[0] == "r":
        document = queries.load_doc(docid)
        document = dict(cPickle.loads(document.get_data()))
        list_items[docid] = {'name' : document['name'], 'amount' : document['amount']}
    request.session['list_items'] = list_items
    return HttpResponseRedirect(
      request.META.get('HTTP_REFERER',reverse('main_list_view'))
    )




