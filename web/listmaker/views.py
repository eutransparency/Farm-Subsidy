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


def activate(request):
    list_name = lists.get_list_name(request)
    lists.create_list(request)
    return HttpResponseRedirect(reverse('lists_home'))


def deactivate(request):
    if request.POST.get('deactivate_confirm'):        
        lists.delete_list(request)
        request.notifications.add("Your list has been deactivated")
        return HttpResponseRedirect(reverse('lists_home'))
    return render_to_response(
        'deactivate_warming.html',
        {},
        context_instance = RequestContext(request)
        )


@login_required
@active_list_required
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
    # 
    # active_list = request.session.get('list_object')
    # if list_id or active_list:
    #     print active_list.pk
    #     list_item = get_object_or_404(models.List, pk=list_id or active_list.pk, user=request.user)
    # else:
    #     list_item = models.List(user=request.user)
    # 
    # if request.POST:
    #     new_list_form = forms.ListForm(request.POST, instance=list_item)
    #     new_list_form.user = request.user
    #     if new_list_form.is_valid():
    #         list_item = new_list_form.save()
    #         
    #         # Save the list object
    #         request.session['list_object'] = list_item
    #         
    #         # Save each item in the list
    #         print request.session.keys()
    #         for item in request.session['list_items']:
    #             item.save()
    #             # models.ListItem.objects.get_or_create(content_type=item.content_)
    #         return HttpResponseRedirect(reverse('list_detail', kwargs={'list_id' : list_item.pk}))
    # else:
    #     print "-=="
    #     print repr(list_item)
    #     new_list_form = forms.ListForm(instance=list_item)
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


def list_view(request, list_id):
    try:
        list_item = models.List.objects.select_related().get(pk=list_id)
    except models.List.DoesNotExist:
        raise Http404

    return render_to_response(
        'list_item.html',
            {
                'list_item': list_item,
            }, context_instance = RequestContext(request))


def edit_list_items(request, list_id=None):
    if list_id:
        try:
            list_object = models.List.objects.get(pk=list_id)
            request.session['list_object'] = list_object
            
        except models.List.DoesNotExist:
            return HttpResponseRedirect(reverse('create_list'))
    request.session['list_enabled'] = True
    list_items = [i for i in list_object.listitem_set.all()]
    request.session['list_items'] = list_items
    # list_total = [i.content_object.amount for i in list_items]
    # request.session['list_total'] = list_total
    
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

    if action == "add":
        # Load the object from the database
        ct = ContentType.objects.get(name=content_type)
        co = ct.get_object_for_this_type(pk=object_id)

        object_hash = {}
        for f in co.list_hash_fields:
            object_hash[f] = co.__dict__[f]

        # Add the URL, if we can get it
        if hasattr(co, 'get_absolute_url'):
            object_hash['get_absolute_url'] = co.get_absolute_url()

        # Add content object and content_type
        object_hash['content_object'] = co.pk
        object_hash['content_type'] = ct.pk
        
        lists.add_item(list_name, object_id, object_hash)

    # if action == "remove":
    #     try:
    #         for i in list_items:
    #             # This is needed becuase an instance of the object
    #             # maybe saved, and there wont be the same
    #             if i.content_type == list_item.content_type and \
    #             i.object_id == list_item.object_id:
    #                 list_items.remove(i)
    #             # list_items.remove(list_item)
    #     except:
    #         pass

    # Create the total for this list
    # list_total = sum([float(i.content_object.amount) for i in list_items])
    
    t = select_template(["blocks/ahah_list.html",])
    c = RequestContext(request, RequestContext(request))
    html = t.render(c)
    
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(json.dumps(
            {
            # 'total' : list_total,
            'html' : html, 
            'action' : action,
            # 'list_item_id' : list_item_id,
            }))
        
    res = HttpResponseRedirect(request.META['HTTP_REFERER'])
    return res
