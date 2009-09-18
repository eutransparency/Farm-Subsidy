#!/usr/bin/env python
# encoding: utf-8

import os
import tempfile
import matplotlib
from matplotlib import rc
from matplotlib.figure import Figure
from matplotlib.cbook import iterable
import matplotlib.numerix as nx
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use('Agg')  # force the antigrain backend
from pylab import *
from matplotlib.patches import Ellipse
from pylab import figure, show, rand
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import show



from django.http import HttpResponse
import locale
locale.setlocale(locale.LC_ALL, '')

from data import models as FarmData

def format_ticks(a,b):
  from django.contrib.humanize.templatetags import humanize
  from django.template.defaultfilters import floatformat
  
  return u"€%s" % humanize.intcomma(floatformat(a))


def make_fig(request, type):
    """ make a chart """
    name_value_dict = {}
    
    years = sorted(request.GET)
    name_value_dict = []
    # assert False
    for year in years:
      name_value_dict.append((year,float(request.GET[year])))
    # assert False

    figure(figsize=(5, 2), linewidth=0) # image dimensions  

    subplots_adjust(left=0.2)

    # add bars
    i = 0
    for key in name_value_dict:
      # if key[0] == "GB":
      #   bar(i+0.25 , key[1], 0.5,  color='red', alpha=0.7, linewidth=0)
      # else:
      bar(i+0.25 , key[1], 0.5,  color='grey', alpha=0.7, linewidth=0)
      i = i+1

    # axis setup
    xticks(arange(0.5, len(name_value_dict)),
        [('%s' % value[0]) 
        for value in name_value_dict],
        size='xx-small')
    max_value = max([v[1] for v in name_value_dict])
    tick_range = arange(0, max_value*1.1, round(max_value,1)/2)
    yticks(tick_range, size='xx-small')
    formatter = FixedFormatter([u"\u20ac%s" % locale.format(u'%d', float(x), True) for x in tick_range])
    gca().yaxis.set_major_formatter(formatter)
    # gca().yaxis.grid(which='major')
    
    response = HttpResponse(mimetype="image/png")
    savefig(response, dpi=120)
    return response



def recipient(request, recipient_id):
  figure(figsize=(1, 1), linewidth=0) # image dimensions  

  payments = FarmData.payment.objects.filter(globalrecipientidx=recipient_id).order_by('year')
  
  fig = plt.figure()
  fig.set_figsize_inches(5,2)  
  ax = fig.add_subplot(1,1,1)

  subplots_adjust(left=0.2, bottom=0.2)

  for loc, spine in ax.spines.iteritems():
      if loc in ['left','bottom']:
          spine.set_position(('outward',0)) # outward by 10 points
      elif loc in ['right','top']:
          spine.set_color('none') # don't draw spine
      else:
          raise ValueError('unknown spine location: %s'%loc)
  
  # turn off ticks where there is no spine
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')
  
  
  for i,payment in enumerate(payments):
    print dir(payment)
    bar(i+0.25,payment.amounteuro, 0.5, color='grey', alpha=0.7, linewidth=0)

  xticks(arange(0.5, len(payments)),
      [('%s' % item.year) 
      for item in payments],
      size='xx-small', rotation=45)
    
  yticks(size='xx-small')
  formatter = FuncFormatter(format_ticks)

  gca().yaxis.set_major_formatter(formatter)

  gca().yaxis.set_major_locator(MaxNLocator(nbins=3, symmetric=True))
  
  
  response = HttpResponse(mimetype="image/png")
  savefig(response, dpi=120)
  return response
  

def country_years(request, country):
  figure(figsize=(1, 1), linewidth=0) # image dimensions  
  
  years = FarmData.data.objects.amount_years(country=country)
  
  fig = plt.figure()
  fig.set_figsize_inches(5,2)  
  ax = fig.add_subplot(1,1,1)

  subplots_adjust(left=0.2, bottom=0.2)
  
  for loc, spine in ax.spines.iteritems():
      if loc in ['left','bottom']:
          spine.set_position(('outward',0)) # outward by 10 points
      elif loc in ['right','top']:
          spine.set_color('none') # don't draw spine
      else:
          raise ValueError('unknown spine location: %s'%loc)
  
  # turn off ticks where there is no spine
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  for i,year in enumerate(years):
    bar(i+0.25,year.amount_euro, 0.5, color='grey', alpha=0.7, linewidth=0)

  xticks(arange(0.5, len(years)),
      [('%s' % item.year) 
      for item in years],
      size='xx-small', rotation=45)
    
  yticks(size='xx-small')
  formatter = FuncFormatter(format_ticks)

  gca().yaxis.set_major_formatter(formatter)

  gca().yaxis.set_major_locator(MaxNLocator(nbins=3, symmetric=True))
  
  response = HttpResponse(mimetype="image/png")
  
  savefig(response, dpi=120)
  return response

def scheme_years(request, globalschemeid):
  figure(figsize=(1, 1), linewidth=0) # image dimensions  
  
  years = FarmData.data.objects.amount_years(scheme=globalschemeid)
  
  fig = plt.figure()
  fig.set_figsize_inches(5,2)  
  ax = fig.add_subplot(1,1,1)

  subplots_adjust(left=0.2, bottom=0.2)
  
  for loc, spine in ax.spines.iteritems():
      if loc in ['left','bottom']:
          spine.set_position(('outward',0)) # outward by 10 points
      elif loc in ['right','top']:
          spine.set_color('none') # don't draw spine
      else:
          raise ValueError('unknown spine location: %s'%loc)
  
  # turn off ticks where there is no spine
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  for i,year in enumerate(years):
    bar(i+0.25,year.amount_euro, 0.5, color='grey', alpha=0.7, linewidth=0)

  xticks(arange(0.5, len(years)),
      [('%s' % item.year) 
      for item in years],
      size='xx-small', rotation=45)
    
  yticks(size='xx-small')
  formatter = FuncFormatter(format_ticks)

  gca().yaxis.set_major_formatter(formatter)

  gca().yaxis.set_major_locator(MaxNLocator(nbins=3, symmetric=True))
  
  response = HttpResponse(mimetype="image/png")
  
  savefig(response, dpi=120)
  return response

