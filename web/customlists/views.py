import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from farmsubsidy.queries import queries
import simplejson
import cPickle

import locale
locale.setlocale(locale.LC_ALL, '')


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
      if key[:4] == "add-":
        document = queries.load_doc(docid)
        document = dict(cPickle.loads(document.get_data()))
        list_items[docid] = {'name' : document['name'], 'amount' : document['amount']}
      if key[:4] == "cur-":
        # The item is currently in the list, now check if it should be deleted
        d = "del-%s" % docid
        if d not in request.POST.keys():
          del list_items[docid]
        
    request.session['list_items'] = list_items
    return HttpResponseRedirect(
      request.META.get('HTTP_REFERER',reverse('main_list_view'))
    )


def list_view_ajax(request):
  return render_to_response('ajax/list.html',
    context_instance=RequestContext(request)
  )


def ajax_add_del(request, action, docid):
  list_items = request.session['list_items']
  
  if action == "add":
    document = queries.load_doc(docid[4:])
    document = dict(cPickle.loads(document.get_data()))
    list_items[docid] = {'name' : document['name'], 'amount' : document['amount']}
  if action == "del":
    del list_items[docid]
  request.session['list_items'] = list_items
  total = 0
  for key,item in list_items.items():
    total += float(item['amount'])
  total = locale.format('%.2f', float(total), True)
  return HttpResponse(simplejson.dumps({'worked' : True, 'total' : total}), mimetype='application/javascript')

