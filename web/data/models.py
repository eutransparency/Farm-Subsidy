from django.db import models
from farmsubsidy.queries import queries
from django.db.models.query import QuerySet

# Create your models here.

class SearchManager(models.Manager):
  
  def __init__(self, results):
    self.results = results
    
  def get_current(self):
      return FakeDocument

  

class FakeDocument(models.Model):
  def __init__(self, id):
      self.model = SearchModelWrapper()
      self.name = "foo"
      self.pk = id

  # def items(self):
  #   return self.id

  
  
  
class SearchModelWrapper(models.Model):
  """docstring for SearchModelWrapper"""

  def __init__(self, results):
    self.id = results['documents'][0]['recipient_id_x']
    objects = SearchManager(results)      
      
      
    # else:
    #   self.id = 0
  
  # def __objects__(self):
  #   return SearchManager(self)


  

  # 'DoesNotExist'
  # 'MultipleObjectsReturned'
  # '__class__'
  # '__delattr__'
  # '__dict__'
  # '__doc__'
  # '__eq__'
  # '__format__'
  # '__getattribute__'
  # '__hash__'
  # '__init__'
  # '__metaclass__'
  # '__module__'
  # '__ne__'
  # '__new__'
  # '__reduce__'
  # '__reduce_ex__'
  # '__repr__'
  # '__setattr__'
  # '__sizeof__'
  # '__str__'
  # '__subclasshook__'
  # '__weakref__'
  # '_collect_sub_objects'
  # '_default_manager'
  # '_get_FIELD_display'
  # '_get_next_or_previous_by_FIELD'
  # '_get_next_or_previous_in_order'
  # '_get_pk_val'
  # '_meta'
  # '_set_pk_val'
  # 'delete'
  # 'objects'
  # 'pk'
  # 'save'
  # 'save_base'



            
# results = queries.do_search('roe')
# search =  SearchModelWrapper(results)
# 
# for key,document in search.documents.items():
#   print document