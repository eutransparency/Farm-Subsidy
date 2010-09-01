"""
Redis read/write interface/backend for lists
"""

import redis

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
        request.session.modified = True

def get_total(list_name):
    try:
        return float(r.get('%s:total' % list_name))
    except:
        return float(0)

def make_total(list_name, method, total=None):
    existing_total = r.get("%s:total" % list_name)
    if existing_total:
        existing_total = float(existing_total)
    else:
        existing_total = float(0)

    if method == "add":
        new_total = existing_total + total
    if method == "remove":
        new_total = existing_total - total
    if method == "recreate":
        print "remaking total"
        tmp_total = 0
        for obj in r.keys('list:1:hashes:*'):
            print tmp_total
            tmp_total += float(r.hget(obj, 'total'))
        print tmp_total
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
    print "adding", list_name, item_key, object_hash
    if not item_in_list(list_name, item_key):
        r.sadd("%s:items" % list_name, item_key)
        for k,v in object_hash.items():
            r.hset("%s:hashes:%s" % (list_name, item_key), k, v)
        r.expire("%s:hashes:%s" % (list_name, item_key), EXPIRE_TIME)

def remove_item(list_name, item_key):
    """
    Deleting an item from a list.
    """
    print "removing", list_name, item_key 
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