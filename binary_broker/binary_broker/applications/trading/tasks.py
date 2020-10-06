from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import random
import json

from binary_broker.celery import *
from .models import *
from .consumers import *

@shared_task
def do_smth():
    print('hello')

@shared_task
def alter_prices():
    queryset = Commodity.objects.all()
    "future work: make this happen in one transaction"
    for cmd in queryset:
        cmd.price = cmd.get_new_price()
        cmd.save(update_fields=['price'])
    channel_layer = get_channel_layer()
    message = {'text': 'lorem ipsum'}
    print(channel_layer)
    print(channel_layer.__dict__)
    async_channel_send('trading_broadcast', 'lorem ipsum')
    async_group_send('trading_broadcast', 'lorem ipsum')
    print(f'message {message} sent')

@shared_task
def alter_prices():
    message = {'text': 'lorem ipsum'}
    channel_layer = get_channel_layer()
    print(channel_layer)
    print(channel_layer.__dict__)
#    async_channel_send('trading_broadcast', 'lorem ipsum')
#    async_group_send('trading', 'lorem ipsum')
    text = 'lorem  ipsum'
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': "trading.do",
            'text': json.dumps(text)
        }
    )

def async_group_send(group_name, text):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "trading.do",
         "text": json.dumps(text)
         })

def async_channel_send(channel_name, text):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name,
        {"type": "trading.do",
         "text": json.dumps(text)
         })
