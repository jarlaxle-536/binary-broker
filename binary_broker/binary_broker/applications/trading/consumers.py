from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
import json

class TradingConsumer(WebsocketConsumer):

    group_name = 'trading'

    def connect(self):
        global channel_layer1
        channel_layer1 = self.channel_layer
        self.accept()
        print(self.group_name)
        print(self.channel_layer)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)
        self.send(text_data='Websocket connection')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

    def trading_do(self, event):
        print('trading do')
        self.send(text_data='hello world')

channel_layer1 = get_channel_layer()
