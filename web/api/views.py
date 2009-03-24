from django.db import models
from farmjango.api.models import blog as apiblog
from farmjango.api.forms import *
from django.shortcuts import render_to_response
from django.utils.html import escape
import sys
sys.path.append('../../')

import queries.querylib
import queries.queries

import datetime

def results(request):
  results = queries.queries.do_search(request.GET['query'])
  # assert False
  return render_to_response('time.html', {'results' : results, 'query' : request.GET['query']})

def allterms(request):
  results = queries.queries.allterms(request.GET['prefix'])
  # assert False
  return render_to_response('allterms.html', {'results' : results, 'query' : request.GET['prefix']})


