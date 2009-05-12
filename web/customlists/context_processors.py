def list_items(request):
  create = request.session.get('create_list', False)
  items = request.session.get('list_items', [])
  list_items = {'create' : create, 'items' : items}
  return {'list_items' : list_items}