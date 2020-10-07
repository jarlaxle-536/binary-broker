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
    channel_layer = get_channel_layer()
    commodities = Commodity.objects.all()
    for cmd in commodities:
        cmd.price = cmd.get_new_price()
        cmd.save()
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': 'trading.update_prices',
            'text': 'updated'
        }
    )
