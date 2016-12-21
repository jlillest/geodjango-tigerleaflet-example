from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView

from django.core.serializers import serialize
from tigerline.models import State
from tigerline.models import County

class Index(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        return { 'title': "Welcome to the tigerleaflet demo!"}

class StateView(TemplateView):
    template_name = "pages/state.html"

    def get_context_data(self, **kwargs):
        return { 'state': self.kwargs['state']}

class CountyView(TemplateView):
    template_name = "pages/county.html"

    def get_context_data(self, **kwargs):
        context = { 'state': self.kwargs['state'],
                    'county': self.kwargs['county'] }
        return context

class StateData(View):
    fields = ('name', 'usps_code', 'fips_code')

    def get(self, request):
        if 'state' in self.request.GET:
            state_code = self.request.GET['state'].upper()
            states = State.objects.raw(
                'SELECT id, ST_simplify(mpoly, 0.01) as mpoly,'
                ' name, usps_code, fips_code'
                ' FROM tigerline_state WHERE usps_code=%s',
                [state_code]
            )
        else:
            states = State.objects.raw(
                'SELECT id, ST_simplify(mpoly, 0.1) AS mpoly,'
                ' name, usps_code, fips_code'
                ' FROM tigerline_state')
        geojson = serialize('geojson',
                            states,
                            geometry_field='mpoly',
                            fields=self.fields)
        return HttpResponse(geojson, content_type='application/json')

class CountyData(View):
    fields = ('name', 'fips_code', 'usps_code')

    def get(self, request):
        if 'county' in self.request.GET:
            usps_code = self.request.GET['state'].upper()
            county_name = self.request.GET['county'].title()
            county_data = County.objects.raw(
                'SELECT tigerline_county.id,'
                ' ST_simplify(tigerline_county.mpoly, 0.01) AS mpoly,'
                ' tigerline_county.name, tigerline_state.usps_code AS usps_code'
                ' FROM tigerline_county JOIN tigerline_state'
                ' ON tigerline_state.fips_code=tigerline_county.state_fips_code'
                ' WHERE tigerline_state.usps_code=%s AND tigerline_county.name=%s',
                [usps_code, county_name],
            )
        elif 'state' in self.request.GET:
            usps_code = self.request.GET['state'].upper()
            county_data = County.objects.raw(
                'SELECT tigerline_county.id,'
                ' ST_simplify(tigerline_county.mpoly, 0.01) AS mpoly,'
                ' tigerline_county.name, tigerline_county.fips_code,'
                ' tigerline_state.usps_code AS usps_code'
                ' FROM tigerline_county JOIN tigerline_state'
                ' ON tigerline_state.fips_code=tigerline_county.state_fips_code'
                ' WHERE tigerline_state.usps_code=%s', [usps_code],
            )
        else:
            raise Http404()
        geojson = serialize('geojson',
                            county_data,
                            geometry_field='mpoly',
                            fields=self.fields)
        return HttpResponse(geojson, content_type='application/json')
