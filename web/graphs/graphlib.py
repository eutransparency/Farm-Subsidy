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
    # assert False
    for year in years:
      name_value_dict[year] = float(request.GET[year])
    # assert False
    # name_value_dict = sorted(name_value_dict.keys())
    
    # import sys
    # sys.exit(name_value_dict)
    
    figure(figsize=(5, 2), linewidth=0) # image dimensions  
    # title(graph_title, size='x-small')
    subplots_adjust(left=0.2)
    # autofmt_xdate()
    
    
    # add bars
    for i, key in enumerate(name_value_dict.keys()):
        bar(i + 0.25 , name_value_dict[key], 0.5,  color='grey', alpha=0.7, linewidth=0)

    # axis setup
    xticks(arange(0.5, len(name_value_dict)),
        [('%s' % name) 
        for name, value in name_value_dict.items()],
        size='xx-small')
    max_value = max(name_value_dict.values())
    tick_range = arange(0, max_value+max_value*1.1, round(max_value,1)/2)
    yticks(tick_range, size='xx-small')
    formatter = FixedFormatter([u"\u20ac%s" % locale.format(u'%d', float(x), True) for x in tick_range])
    gca().yaxis.set_major_formatter(formatter)
    # gca().yaxis.grid(which='major')
    


    
    response = HttpResponse(mimetype="image/png")
    savefig(response, dpi=120)
    return response
