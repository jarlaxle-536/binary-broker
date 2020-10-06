from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
import json

class TradingConsumer(WebsocketConsumer):

    group_name = 'trading'

    def connect(self):

        self.channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print('channel layer after connect:', self.channel_layer.__dict__)
        self.accept()
        self.send(text_data='RECEIVED')

    def receive(self, text_data=None, bytes_data=None):
        print('triggered RECEIVE')
        self.send(text_data="Hello world!")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.close()

    def trading_do(self, event):
        print('trading do')
        self.send_json(
            {
                'type': 'trading.do',
                'text': event['content']
            }
        )
