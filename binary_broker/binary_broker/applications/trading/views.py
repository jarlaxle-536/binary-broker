from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from rest_framework.response import Response

import json

from .serializers import *
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
        print(self.__dict__)
        instances = Commodity.objects.all()
        serializer = CommoditySerializer(instances, many=True)
        rendered = ''
        for data in serializer.data:
            rendered += render_navbar_item(request, data)
        return Response(rendered)

    def put(self, request, *args, **kwargs):
        instances = []
        serializer = DemoSerializer(instances, many=True)
        return Response(serializer.data)

def render_navbar_item(request, data):
    html = loader.get_template('commodity/navbar_item.html').template.source
    commodity = Commodity.objects.get(pk=data['id'])
    context = {
        '[commodity_detail_url]': reverse(
            'commodity_detail', kwargs={'pk': commodity.pk}),
        '[commodity_description]': str(commodity)
    }
    for k, v in context.items():
        html = html.replace(k, v)
    return html

class CommodityDetailView(DetailView):

    model = Commodity
    template_name = 'commodity/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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
