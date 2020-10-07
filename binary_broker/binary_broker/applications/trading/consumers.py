from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
import json

from .models import *

class TradingConsumer(WebsocketConsumer):

    group_name = 'trading'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)
        self.send(text_data='Websocket connection')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

    def trading_update_prices(self, event):
        print(f'trading:update_prices with {event}')
        prices_dict = {cmd.pk: cmd.price for cmd in Commodity.objects.all()}
        print(prices_dict)
        self.send(text_data='hello world')
