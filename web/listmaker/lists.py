"""
Redis read/write interface/backend for lists
"""

import redis
from django.contrib.contenttypes.models import ContentType

import models

EXPIRE_TIME = 60*60*24*10

r = redis.Redis()

def get_list_name(request):
    """
    Returns a valid list name.
    
    If there is already an active list, then return its name, otherwise 
    create a name based on the requst object.
    
    """
    
    if request.session.get('list_name'):
        return request.session['list_name']
    
    if request.user.is_anonymous():
        list_name = "list:%s" % request.session.session_key
    else:
        list_name = "list:%s" % request.user.pk
    return list_name

def create_list(request):
    list_name = get_list_name(request)
    request.session['list_name'] = list_name
    request.session.modified = True
    
def delete_list(request):
    if request.session.get('list_name'):
        for k in r.keys("%s:*" % request.session['list_name']):
            r.delete(k)
        r.delete(request.session['list_name'])
        del request.session['list_name']
        try:
            del request.session['list_object']
        except:
            pass
        request.session.modified = True

def get_total(list_name):
    try:
        return float(r.get('%s:total' % list_name))
    except:
        return float(0)

def make_total(list_name, method, total=None):

    tmp_total = 0
    for obj in r.keys('%s:hashes:*' % list_name):
        t =  r.hget(obj, 'total')
        try:
            tmp_total += float(t)
        except:
            tmp_total += float(0)
    new_total = tmp_total
    
    r.delete("%s:total" % list_name)
    r.set("%s:total" % list_name, new_total)
    return new_total

def list_items(list_name):
    """
    Returns a list of dicts of each item in _list_name_
    """
    items = []
    for item in r.keys("%s:hashes:*" % list_name):
        items.append(r.hgetall(item))
    return items
    
def item_in_list(list_name, item_key):
    return r.sismember("%s:items" % list_name, item_key)

def add_item(list_name, item_key, object_hash):
    if not item_in_list(list_name, item_key):
        r.sadd("%s:items" % list_name, item_key)
        for k,v in object_hash.items():
            r.hset("%s:hashes:%s" % (list_name, item_key), k, v)
        r.expire("%s:hashes:%s" % (list_name, item_key), EXPIRE_TIME)
    make_total(list_name, 'add')

def remove_item(list_name, item_key):
    """
    Deleting an item from a list.
    """
    # remove the hash
    r.delete("%s:hashes:%s" % (list_name, item_key))
    # remove the item from the list_items set
    r.srem("%s:items" % list_name, item_key)
    

def save_items(list_object, list_name):
    """
    Converts whatever is in redis in to ListItem DB objects (IE, GFKs to the
    content object)
    
    Requires a List object
    """
    list_object.save()

    active_list_items = list_items(list_name)

    # Delete all existing ListItems relating to this list
    list_object.listitem_set.all().delete()
    
    for item in active_list_items:
        i = models.ListItem()
        if item.get('content_type') and item.get('content_object'):
            i.content_type_id = item.get('content_type')
            i.object_id = item.get('content_object')
            i.list_id = list_object
            i.save()
        # i = models.ListItem()


def make_object_hash(model_object, ct=None):
    """
    Takes a model object and returns dict ready to be passed to add_item()
    """
    if not ct:
        ct = ContentType.objects.get_for_model(model_object)
    
    object_hash = {}
    for f in model_object.list_hash_fields:
        object_hash[f] = model_object.__dict__[f]

    # Add the URL, if we can get it
    if hasattr(model_object, 'get_absolute_url'):
        object_hash['get_absolute_url'] = model_object.get_absolute_url()

    # Add content object and content_type
    object_hash['content_object'] = model_object.pk
    object_hash['content_type'] = ct.pk
    

    
    return object_hash

def make_item_key(model_object, ct=None):
    """
    Makes an item key from a given model.
    
    This is in the form of "[content type pk]:[object pk]", in a
    GFK style.
    
    NOTE: this will break other things if the pk of the object 
    has a colon (:) in it.
    """
    
    if not ct:
        ct = ContentType.objects.get_for_model(model_object)

    item_key = "%s:%s" % (ct.pk, model_object.pk)
    return item_key