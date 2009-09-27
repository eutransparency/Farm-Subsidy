from django.template import Library, Node
register = Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'selected'
    return ''
