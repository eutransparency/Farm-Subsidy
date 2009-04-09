import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from cart import Cart
from groups.models import Recipient


def test(request):
  cart = Cart(request)
  recipient = Recipient.objects.get()
  cart.add(recipient, '1', '1')
  return render_to_response('cart_base.html', context_instance=RequestContext(request))    
  

# def add_to_cart(request, product_id, quantity):
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     cart.add(product, product.unit_price, quantity)
# 
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     cart.remove(product)
# 
# def get_cart(request):
#     return render_to_response('cart.html', dict(cart=Cart(request)))