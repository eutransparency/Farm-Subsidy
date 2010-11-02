# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string, select_template
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import json
import models
import forms
from django.contrib.auth.decorators import login_required

import lists

def active_list_required(view):
    """
    Decorator that checks for a list, and redirects to the list home if one 
    doesn't exist.
    """
    def _decorated(request, *arg, **kw):
        if not request.session.get('list_name'):
            return HttpResponseRedirect(reverse('lists_home'))
        return view(request, *arg, **kw)
    return _decorated


def lists_home(request):
    lists.list_items('test')
    return render_to_response(
    'lists_home.html', 
    {}, 
    context_instance = RequestContext(request)
    )


def all_lists(request):
    all_lists_qs = models.List.objects.all()
    return render_to_response(
        'all_lists.html', 
        {'lists' : all_lists_qs},
        context_instance = RequestContext(request)
    )

def activate(request):
    list_name = lists.get_list_name(request)
    lists.create_list(request)
    return HttpResponseRedirect(reverse('lists_home'))


def deactivate(request):
    if request.POST.get('deactivate_confirm'):
        if request.POST['deactivate_confirm'].lower() == "save":
            return HttpResponseRedirect(reverse('save_list'))
        lists.delete_list(request)
        request.notifications.add("Your list has been deactivated")
        return HttpResponseRedirect(reverse('lists_home'))
    return render_to_response(
        'deactivate_warning.html',
        {},
        context_instance = RequestContext(request)
        )


@login_required
def manage_lists(request, list_id=None):
    """
    Update or create a list.
    
    Handles the POST for the create/edit page, and displaies the correct form.
    """

    if list_id:
        list_object = get_object_or_404(models.List, pk=list_id, user=request.user)
    else:
        list_object = models.List(user=request.user)
    
    form = forms.ListForm(instance=list_object)

    if request.POST:
        form = forms.ListForm(request.POST, instance=list_object)
        if form.is_valid():
            if request.session.get('list_name'):
                lists.save_items(list_object, request.session.get('list_name'))
            
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())

    return render_to_response(
        'edit.html', 
            {
                'new_list_form': form, 
            }, context_instance = RequestContext(request))


@login_required
def my_lists(request):
    lists = models.List.objects.filter(user=request.user)
    return render_to_response(
        'mylists.html',
            {
                'lists': lists,
            }, context_instance = RequestContext(request))


def list_view(request, list_id, slug=None):
    try:
        list_item = models.List.objects.select_related().get(pk=list_id)
    except models.List.DoesNotExist:
        raise Http404

    list_total = sum([i.content_object.total for i in list_item.listitem_set.all()])
    
    return render_to_response(
        'list_item.html',
            {
                'list_item': list_item,
                'list_total': list_total,
            }, context_instance = RequestContext(request))


def edit_list_items(request, list_id=None):
    """
    'activates' a saved list.
    """
    if list_id:
        try:
            list_object = models.List.objects.get(pk=list_id)
            request.session['list_object'] = list_object
        except models.List.DoesNotExist:
            return HttpResponseRedirect(reverse('create_list'))

    list_name = lists.get_list_name(request)
    
    for list_item in list_object.listitem_set.all().select_related():
        co = list_item.content_object
        item_key = lists.make_item_key(co)
        object_hash = lists.make_object_hash(co)
        lists.add_item(list_name, item_key, object_hash)
    
    request.session['list_name'] = list_name    
    request.session['list_enabled'] = True    
    request.session['list_object'] = list_object    
    request.session.modified = True

    return HttpResponseRedirect(reverse('list_detail', args=(list_object.pk,)))


@active_list_required
def add_remove_item(request):
    """
    Expects POST data with the following values:
        * content_type
        * object_id
        
    Only content types (models) with a valid `LIST_ENABLED` attribute will be allowed
    """
    
    # The list we're working with
    list_name = lists.get_list_name(request)
    
    # Grab the POST data we'll need
    
    # Action is 'add' or 'remove'
    action = request.POST.get('action', 'add')

    content_type = request.POST.get('content_type', None)
    object_id = request.POST.get('object_id', None)

    # Load the object from the database
    ct = ContentType.objects.get(name=content_type)
    co = ct.get_object_for_this_type(pk=object_id)
    item_key = lists.make_item_key(co, ct)
    
    if action == "add":
        object_hash = lists.make_object_hash(co)
        lists.add_item(list_name, item_key, object_hash)

    if action == "remove":
        lists.remove_item(list_name, item_key)

    # Create the total for this list
    if hasattr(co, 'list_total_field'):
        total_field = getattr(co, co.list_total_field)
        list_total = lists.make_total(list_name, action, total_field)
    
    t = select_template(["blocks/ahah_list.html",])
    c = RequestContext(request, RequestContext(request))
    html = t.render(c)
    
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(json.dumps(
            {
            'total' : list_total,
            'html' : html, 
            'action' : action,
            'list_item_id' : item_key,
            }))
        
    res = HttpResponseRedirect(request.META['HTTP_REFERER'])
    return res
