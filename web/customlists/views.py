import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from web.search import queries
import simplejson
import cPickle
from data import models as FarmData

import locale
locale.setlocale(locale.LC_ALL, '')


def main(request):
  if request.method == "POST":
    if request.POST.get('create_list', False):      
      request.session['create_list'] = True
      request.session['custom_list_items'] = {}
    if request.POST.get('delete_list', False):      
      del request.session['create_list']
      del request.session['custom_list_items']
      del request.session['custom_list_items_total']
      
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
        document = FarmData.recipient.objects.select_related().get(globalrecipientidx=docid[4:])
        # document = dict(cPickle.loads(document.get_data()))
        list_items[docid] = {'name' : document.name, 'amount' : document.globalrecipientidx.amount_euro}
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
  # del request.session['custom_list_items']['GB271466']
  docid = docid[4:]
  list_items = request.session['custom_list_items']
  if action == "add":
    document = FarmData.recipient.objects.select_related().get(globalrecipientidx=docid)
    list_items[docid] = {'name' : document.name, 'amount' : document.globalrecipientidx.amount_euro}
    
  if action == "del":
    del list_items[docid]
  request.session['custom_list_items'] = list_items
  total = 0
  for key,item in list_items.items():
    total += float(item['amount'])
  total = locale.format('%.2f', float(total), True)
  request.session['custom_list_items_total'] = total
  return HttpResponse(simplejson.dumps({'worked' : True, 'total' : total}), mimetype='application/javascript')






