#!/usr/bin/env python
# encoding: utf-8
import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'farmsubsidy.web.settings'

import farmsubsidy.web.feeds.models as feeds
import feedparser
import datetime
import calendar
import time

allfeeds = feeds.Feeds.objects.filter(is_active=True)

for f in allfeeds:

  try:
    last_mod = time.strptime(str(f.last_modified), "%Y-%m-%d %H:%M:%S")
  except:
    last_mod = None
  
  d = feedparser.parse(f.url)
  
  if len(d.entries) > 0:
    print "\nUPDATING %s\n" % f.title
    
    if 'etag' in d:
      f.etag = d.etag
      f.save()
    
    if 'modified' in d:
      f.last_modified = datetime.datetime.utcfromtimestamp(calendar.timegm(d.modified))
      f.save()

    for e in d.entries:

      if len(feeds.FeedItems.objects.filter(guid=e.guid)) == 0:      
        date = datetime.datetime(*e.updated_parsed[:7])
      
        if 'tags' in e:
          
          for tag in e.tags:
            if tag['term'][:3] == "pub":
              try:
                date = time.strptime(str(tag['term']), "pub%Y%m%d")
                date = time.strftime("%Y-%m-%d %H:%M:%S",date)
              except:
                print tag['term']
          
          tags = ", ".join([t.term for t in e.tags])
        else:
          tags = ""
        
        if 'summary' in e:
          summary = e.summary
        else:
          summary = ''
          
                  
        item = feeds.FeedItems(
           title = e.title[:80],
           description=summary,
           date = date,
           guid=e.guid,
           feed=f,
           url = e.link,
           tags = tags
           )
        item.save()  
  
