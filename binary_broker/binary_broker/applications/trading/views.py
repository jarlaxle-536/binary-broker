from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.models import AjaxDataSource
from bokeh.embed import components
from bokeh.resources import INLINE

from .serializers import *
from .models import *

class CommodityPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    def patch(self, request, *args, **kwargs):
        print('calling commodity partial update w/patch')
        instances = Commodity.objects.all()
        serializer = CommoditySerializer(instances, many=True)
        return Response(serializer.data)

class CommodityListView(ListView):

    template_name = 'commodity/list.html'

    def get_queryset(self):
        return Commodity.objects.all()

class CommodityDetailView(DetailView):

    model = Commodity
    template_name = 'commodity/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        prices_history = kwargs['object'].get_last_records(
            datetime.timedelta(seconds=60))
        prices_history.sort(key=lambda t: t[0])
        context['price_plot_script'], context['price_plot_div'] = \
            create_prices_plot_components(prices_history)
        return context

def get_prices_plot_and_script(request, pk):
    print(f'getting prices plot for {pk}')
    commodity = Commodity.objects.get(pk=pk)
    prices_history = commodity.get_last_records(
        datetime.timedelta(seconds=60))
    plot_components = create_prices_plot_components(prices_history)
    return HttpResponse(plot_components)

def create_prices_plot_components(prices_history):
    prices_plot = figure(x_axis_type='datetime', plot_width=600, plot_height=350)
    prices_plot.line(*list(zip(*prices_history)))
    plot_components = list(components(prices_plot))
    plot_components[0] = get_rid_of_outer_tags(plot_components[0])
    return plot_components

def get_rid_of_outer_tags(text):
    return '<'.join('>'.join(text.split('>')[1:]).split('<')[:-1])
