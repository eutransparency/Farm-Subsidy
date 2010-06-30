"""
Redis read/write interface/backend for lists
"""

import redis

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
        r.delete(request.session['list_name'])
        del request.session['list_name']
        request.session.modified = True

def list_items(list_name):
    """
    Returns a list of dicts of each item in _list_name_
    """
    items = []
    for item in r.keys("%s:hashes:*" % list_name):
        print r.hgetall(item)

def item_in_list(list_name, item_key):
    return r.sismember("%s:items" % list_name, item_key)

def add_item(list_name, item_key, object_hash):
    print "adding", list_name, item_key, object_hash
    if not item_in_list(list_name, item_key):
        r.sadd("%s:items" % list_name, item_key)
        for k,v in object_hash.items():
            r.hset("%s:hashes:%s" % (list_name, item_key), k, v)
        r.expire("%s:hashes:%s" % (list_name, item_key), EXPIRE_TIME)

