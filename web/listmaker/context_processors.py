from models import List, ListItem

def list_items(request):
    # request.session['list_items'] = []
    if request.session.get('list_name'):
        return {
            'list_enabled' : True,
            # 'list_object' : request.session.get('list_object'),
            # 'list_items' : request.session.get('list_items'),
        }
    else:
        return {}