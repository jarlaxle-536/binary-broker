from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import asyncio

class TradingConsumer(WebsocketConsumer):

    def connect(self):
        self.channel_group_name = 'trading_broadcast'
        self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data='RECEIVED')
#        self.close()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="Hello world!")
        print('RECEIVED')
        self.close()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.channel_group_name,
            self.channel_name
        )
