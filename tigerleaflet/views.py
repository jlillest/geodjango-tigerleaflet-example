from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import TemplateView

from tigerleaflet.models import State
from tigerleaflet.models import County

def get_geojson(data, fields):
    return serialize('geojson', data, geometry_field='mpoly', fields=fields)


class CountryView(TemplateView):
    template_name = "countryview_default.html"

    def get_context_data(self, **kwargs):
        return { 'title': "US States"}


class CountryData(View):
    fields = ('name', 'usps_code', 'fips_code')

    def post(self, request):
        map_data = State.objects.raw(
            'SELECT id, ST_simplify(mpoly, 0.1) AS mpoly,'
            ' name, usps_code, fips_code'
            ' FROM tigerleaflet_state')
        geojson = get_geojson(map_data, self.fields)

        return HttpResponse(geojson, content_type='application/json')


class StateView(TemplateView):
    template_name = "stateview_default.html"

    def get_context_data(self, **kwargs):
        state_code = self.kwargs['state']
        state_name = State.objects.get(usps_code=state_code.upper()).name
        context = { 'title': "Showing " + state_name,
                    'state': state_code
                    }
        return context


class StateData(View):
    fields = ('name', 'usps_code', 'fips_code')

    def post(self, request):
        usps_code = self.request.POST['state'].upper()
        map_data = County.objects.raw(
            'SELECT id, ST_simplify(mpoly, 0.01) AS mpoly,'
            ' name, fips_code, usps_code FROM tigerleaflet_county'
            ' WHERE usps_code=%s', [usps_code],
        )
        geojson = get_geojson(map_data, self.fields)

        return HttpResponse(geojson, content_type='application/json')


class CountyView(TemplateView):
    template_name = "countyview_default.html"

    def get_context_data(self, **kwargs):
        state_code = self.kwargs['state']
        county = self.kwargs['county']
        state_name = State.objects.get(usps_code=state_code.upper()).name
        county_name = county.replace('_', ' ').title()
        context = { 'title' : county_name + ", " + state_name,
                    'state' : state_code,
                    'county': county,
                    }
        return context


class CountyData(View):
    fields = ('name', 'fips_code', 'usps_code')

    def post(self, request):
        usps_code = self.request.POST['state'].upper()
        county_name = self.request.POST['county'].replace("_", " ").title()
        map_data = County.objects.raw(
            'SELECT id, mpoly,'
            ' name, usps_code FROM tigerleaflet_county'
            ' WHERE usps_code=%s AND name=%s',
            [usps_code, county_name],
        )
        geojson = get_geojson(map_data, self.fields)

        return HttpResponse(geojson, content_type='application/json')
