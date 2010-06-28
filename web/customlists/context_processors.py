def custom_list(request):
  custom_list = {}
  if request.session.get('create_list', False):
    custom_list['active'] = True
    custom_list['list_items'] = request.session.get('custom_list_items', {})
    custom_list['total'] = request.session.get('custom_list_items_total', 0)    
  return {'custom_list' : custom_list}