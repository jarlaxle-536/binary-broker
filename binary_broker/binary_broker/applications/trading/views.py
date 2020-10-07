from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import json

from .models import *

class CommodityListView(ListView):

    template_name = 'commodity/list.html'

    def get_queryset(self):
        return Commodity.objects.all()

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
