from piston.emitters import Emitter
from django.shortcuts import render_to_response

KML_MIMETYPE = 'application/vnd.google-earth.kml+xml; charset=utf-8'

class KMLEmitter(Emitter):

    def serialize_geometry(self, geometry):
        return geometry.kml

    def render(self, request):
        data = self.construct()
        if hasattr(self.handler, 'model'):
            title = self.handler.model._meta.verbose_name_plural
        else:
            title = "test"

        if isinstance(data, dict):
            data = [v for k,v in data.items()]

        context = {
            'document_title': title,
            'places': data,
        }

        return render_to_response('kml.html', context, mimetype=KML_MIMETYPE)

Emitter.register('kml', KMLEmitter, KML_MIMETYPE)