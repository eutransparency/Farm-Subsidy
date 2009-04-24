#!/usr/bin/env python
# encoding: utf-8

import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # force the antigrain backend
from matplotlib import rc
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.cbook import iterable
import matplotlib.numerix as nx
from pylab import *
from django.http import HttpResponse
from pylab import figure, show, rand
from matplotlib.patches import Ellipse
import locale
locale.setlocale(locale.LC_ALL, '')

  

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
      bar(i+0.25 , key[1], 0.5,  color='grey', alpha=0.7, linewidth=0)
      i = i+1

    # axis setup
    xticks(arange(0.5, len(name_value_dict)),
        [('%s' % value[0]) 
        for value in name_value_dict],
        size='xx-small')
    max_value = max([v[1] for v in name_value_dict])
    tick_range = arange(0, max_value+max_value*1.1, round(max_value,1)/2)
    yticks(tick_range, size='xx-small')
    formatter = FixedFormatter([u"\u20ac%s" % locale.format(u'%d', float(x), True) for x in tick_range])
    gca().yaxis.set_major_formatter(formatter)
    # gca().yaxis.grid(which='major')
    


    
    response = HttpResponse(mimetype="image/png")
    savefig(response, dpi=120)
    return response
