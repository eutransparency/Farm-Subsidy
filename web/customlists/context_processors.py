def list_items(request):
  # del request.session['create_list']
  # del request.session['list_items']
  create = request.session.get('create_list', False)
  items = request.session.get('list_items', [])
  list_items = {'create' : create, 'items' : items}
  return {'list_items' : list_items}