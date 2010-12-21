import csv
import StringIO

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template import Context, Template
from django.template.loader import render_to_string, select_template
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.encoding import smart_unicode
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml

from data.models import Recipient, GeoRecipient, Payment

# def geo(request, lng, lat, format='kml'):
#     lng, lat = map(float, (lng, lat,))
#     limit = request.GET.get('limit', 10)
#     offset = request.GET.get('offset', 0)
#     
# 
#     base_qs = GeoRecipient.objects.distance(Point((lng, lat))).order_by('-distance')
#     
#     if format == 'kml':
#         qs = base_qs.kml()
#     if format == 'json':
#         qs = base_qs.json()
#         print "json"
#     
#     qs = qs[offset:limit]
#     
#     djf = Django.Django(geodjango="geometry", properties=['city', 'state'])
#     geoj = GeoJSON.GeoJSON()
#     string = geoj.encode(djf.decode(qs))
#     print string
#     
#     # return render_to_kml('kml.html', {'qs' : qs}) 

def csv_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)    
    recipient_fields = ('globalrecipientidx',
                        'name',
                        'address1',
                        'address2',
                        'zipcode',
                        'town',
                        'countryrecipient',
                        'countrypayment',
                        'geo1',
                        'geo2',
                        'geo3',
                        'geo4',
                        'lat',
                        'lng',
                        'total',
                        )

    payment_fields = ('scheme',
                      'amounteuro',
                      'amountnationalcurrency',
                      'year',
                      'countrypayment',
                      )

    recipient_info = []
    from django.utils.encoding import smart_unicode, smart_str
    for field in recipient_fields:
        field_value = u"%s" % recipient.__dict__[field]
        field_value = field_value.encode('utf8')
        recipient_info.append(field_value)
    
    
    # response = HttpResponse(mimetype='text/csv')
    response = HttpResponse(mimetype='text/csv')
    # response['Content-Disposition'] = 'attachment; filename=recipient-%s.csv' % recipient.pk

    csv_writer = csv.writer(response)

    
    csv_writer.writerow(recipient_fields + payment_fields)

    for payment in recipient.payment_set.all():
        csv_data = []
        csv_data = recipient_info + csv_data

        for field in payment_fields:
            if field == "scheme":
                csv_data.append(payment.scheme.nameenglish.encode('utf8'))
            else:
                csv_data.append(payment.__dict__[field])

        csv_writer.writerow(csv_data)

    return response



def documentation(request, path):
    """
    A version of direct_to_template, I guess.
    
    Takes a path, and looks for a tempalte that might match it, then rendars it.
    
    Simples.
    """
    if path.endswith('/') and len(path) > 1:
        path = path[:-1]
    tempalte_guesses = [path]
    # tempalte_guesses.append("%s.html" % path)
    tempalte_guesses.append("documentation/%s.html" % path)
    tempalte_guesses.append("documentation/%s/index.html" % path)
    c = RequestContext(request)
    t = select_template(tempalte_guesses)
    return HttpResponse(t.render(c))

    return t.render()





