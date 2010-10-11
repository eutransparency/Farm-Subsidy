from django.template.loader import select_template
from django.core.cache import cache
import hashlib

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

    def __init__(self, queryset):
        self.queryset = queryset

    def __getitem__(self, k):
        if not isinstance(k, slice):
            raise TypeError

        return self.queryset[k.start:k.stop]

    def count(self):
        key = "count.%s" % hash(str(self.queryset.query))
        count = cache.get(key)
        if not count:
            count = self.queryset.count()
            cache.set(key, count, 60)
        return count

    def __len__(self):
        return self.count()


