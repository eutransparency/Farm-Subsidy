from models import List, ListItem

def list_items(request):
    """
    Mainly gives the RequestContext information on if there is an active list
    by settings 'list_enabled' if there is a 'list_name' set in the session.
    """
    if request.session.get('list_name'):
        return {
            'list_enabled' : True,
            'list_name' : request.session.get('list_name'),
        }
    else:
        return {}