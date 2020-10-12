from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction
from celery import shared_task
import asyncio
import random
import json

from binary_broker.celery import *
from .consumers import *
from .models import *

@app.task
def alter_prices():
    commodities = Commodity.objects.all()
    with transaction.atomic():
        for cmd in commodities:
            cmd.price = cmd.get_new_price()
            cmd.save()

@app.task
def update_trading():
    async_to_sync(channel_layer.group_send)(
        'trading', {
            'type': 'trading.update_all',
            'text': 'updated'
        }
    )

channel_layer = get_channel_layer()
