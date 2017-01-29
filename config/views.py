from django.views.generic import TemplateView
from tigerleaflet.models import State
from tigerleaflet.models import County

class Index(TemplateView):
    template_name = "pages/country.html"

    def get_context_data(self, **kwargs):
        return { 'title': "Welcome to the tigerleaflet demo!"}

class StateView(TemplateView):
    template_name = "pages/state.html"

    def get_context_data(self, **kwargs):
        state_code = self.kwargs['state']
        state_name = State.objects.get(usps_code=state_code.upper()).name
        context = { 'title': "Showing " + state_name,
                    'state': state_code
                    }
        return context

class CountyView(TemplateView):
    template_name = "pages/county.html"

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
