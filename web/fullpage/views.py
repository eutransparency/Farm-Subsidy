from django.shortcuts import render_to_response
from django.template.loader import render_to_string
# Create your views here.



class lastet:
    def __init__(self):
        self.items = ['a','b','c']

    def render(self):
        return render_to_string('fullpage/latest.html', {'items': self.items})

  

def fullpage(request):
  """docstring for lastetcomments"""
  sidebar = [lastet()]
  return render_to_response('fullpage/page.html', {'sidebar' : sidebar})
