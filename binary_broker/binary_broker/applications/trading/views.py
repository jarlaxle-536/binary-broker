from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

        context['price_plot'] = create_prices_plot(prices_history)
        return context

def get_prices_plot(request, pk):
    print(f'getting prices plot for {pk}')
    commodity = Commodity.objects.get(pk=pk)
    prices_history = commodity.get_last_records(
        datetime.timedelta(seconds=60))
    return create_prices_plot(prices_history)

def create_prices_plot(prices_history):
    fig = Figure()
    ax = fig.add_subplot(111)

    x = []
    y = []

    x = [k[1] for k in prices_history]
    y = [k[0] for k in prices_history]

    ax.plot_date(x, y, '-')
#    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
