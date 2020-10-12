from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import components

from rest_framework.response import Response

import json

from .serializers import *
from .auxiliary import *
from .models import *

class CommodityListView(ListView):

    template_name = 'commodity/list.html'

    def get_queryset(self):
        return Commodity.objects.all()

class CommodityPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    def patch(self, request, *args, **kwargs):
        print('calling commodity partial update w/patch')
        instances = Commodity.objects.all()
        serializer = CommoditySerializer(instances, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instances = []
        serializer = DemoSerializer(instances, many=True)
        return Response(serializer.data)

class CommodityDetailView(DetailView):

    model = Commodity
    template_name = 'commodity/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        prices_history = kwargs['object'].get_last_records(
            datetime.timedelta(seconds=60))
        prices_history.sort(key=lambda t: t[0])
        prices_plot = figure(
            x_axis_type='datetime',
            plot_width=600,
            plot_height=350
        )
        prices_plot.line(*list(zip(*prices_history)))
        prices_plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        print(*[i[0] for i in prices_history], sep='\n')
        context['price_plot_script'], context['price_plot_div'] = \
        components(prices_plot)
        return context

def websocket_test(request):
    print('websocket test')
    print(f'is ajax: {request.is_ajax()}')
    text = 'lorem  ipsum'
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': "trading.do",
            'text': json.dumps(text)
        })
    print(f'Sent message to client: {text}')

    return HttpResponse('lorem ipsum')
