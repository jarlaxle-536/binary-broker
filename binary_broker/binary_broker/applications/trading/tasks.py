from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import random

from binary_broker.celery import *
from binary_broker.channel_routing import application as channel_app
from .models import *
from .consumers import *

@shared_task
def do_smth():
    print('hello')

@app.task
def alter_prices():
    queryset = Commodity.objects.all()
    "future work: make this happen in one transaction"
    for cmd in queryset:
        cmd.price = cmd.get_new_price()
        cmd.save(update_fields=['price'])
    print(channel_app)
    print(channel_app.__dict__)
    channel_layer = get_channel_layer()
    message = {'text': 'lorem ipsum'}
    print(channel_layer)
    print(channel_layer.__dict__)
    channel_layer.group_send('trading_broadcast', message)
