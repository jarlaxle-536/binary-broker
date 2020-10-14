from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .serializers import *
from .auxiliary import *
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

        context['price_plot'] = create_price_plot(prices_history)
        return context

def create_price_plot_response(request, pk):
    commodity = Commodity.objects.get(pk=pk)
    price_history = commodity.get_last_records(
        datetime.timedelta(seconds=60))
    plot = create_price_plot(price_history)
    canvas = FigureCanvas(plot)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
