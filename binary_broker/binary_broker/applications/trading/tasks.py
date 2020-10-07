from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import asyncio
import random
import json

from binary_broker.celery import *
from .consumers import *
from .models import *

@shared_task
def do_smth():
    print('hello')

@app.task
def alter_prices():
    text = 'lorem  ipsum'
    channel_layer = get_channel_layer()
    print(channel_layer, channel_layer1)
    print(channel_layer.__dict__)
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': "trading.do",
            'text': json.dumps(text)
        }
    )
