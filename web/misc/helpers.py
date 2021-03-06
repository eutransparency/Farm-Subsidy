import hashlib
import cPickle

from django.conf import settings
from django.template.loader import select_template
from django.core.cache import cache

from django.utils.encoding import force_unicode

def make_key(qs, key=None):
    if key:
        key = force_unicode(key)
        return "%s.%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, key)
    else:
        return qs.__hash__()


def country_template(path, country):
    """
    Wrapper function for select_template.
    
    Given a path, split on '/', prefix the last part (the file name) with 
    __country__, pass it to select_template and return a string for use with 
    render_to_response.
    
    For Example:
        country_template('locations/all_locations.html', 'GB')
    Will look for:
        locations/GB_all_locations.html
    Then:
        locations/all_locations.html

    """
    
    # First parse the path
    path = path.split('/')
    filename = path[-1]
    names_to_try = ["%s_%s" % (country, filename), filename]
    return select_template(names_to_try).name


class CachedCountQuerySetWrapper(object):

    def __init__(self, queryset, key=None):
        self.queryset = queryset
        self.key = make_key(queryset, key)

    def __getattr__(self, name):
        """
        Hack to pretend this is actually a queryset object
        """
        return getattr(self.queryset, name)
    
    def __getitem__(self, k):
        if not isinstance(k, slice):
            return self.queryset[k]

        return self.queryset[k.start:k.stop]

    def count(self):
        key = make_key(self.key)
        count = cache.get(key)
        if not count:
            count = self.queryset.count()
            cache.set(key, count, 0)
        return count

    def __len__(self):
        return self.count()



def QuerySetCache(qs, key=None, cache_type='deafult'):
    """
    Caches the *whole* queryset as it is given to the function.
    
    For this to work, make sure it's called as late as it can be.
    
    Calling this on paged queries will work, but is silly, as the cached 
    queryset will normally be slower than just not caching it.
    
    Use CachedCountQuerySetWrapper for speeding up paged results.
    
    You have been warned.
    """

    key = make_key(qs, key)

    def write_to_cache(file_path, qs):
        f = open(file_path, 'w')
        f.write(cPickle.dumps(qs))
        return qs
        
    
    # Use the django built in cache
    if cache_type == 'deafult':
        cached_qs = cache.get(key)
        if cached_qs:
            cached_qs = cPickle.loads(cached_qs)
        else:
            cached_qs = qs
            cache.set(key, cPickle.dumps(cached_qs))
        return cached_qs
    
    # Use the file system, for more permanant caching
    if cache_type == 'filesystem':
        import os
        file_path = "%s/%s" % (settings.FILE_CACHE_PATH, key)
        if os.path.exists(file_path):
            try:
                return cPickle.loads(open(file_path).read())
            except EOFError:
                # The file wasn't written cleanly, so remake it
                return write_to_cache(file_path, qs)
        else:
            return write_to_cache(file_path, qs)
