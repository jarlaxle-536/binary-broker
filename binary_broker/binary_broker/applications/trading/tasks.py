from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import random
import json

from binary_broker.celery import *
from .models import *

@shared_task
def do_smth():
    print('hello')

@shared_task
def alter_prices():
    text = 'lorem  ipsum'
    print(channel_layer.__dict__)
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': "trading.do",
            'text': json.dumps(text)
        }
    )

channel_layer = get_channel_layer()
