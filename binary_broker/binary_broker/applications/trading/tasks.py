from binary_broker.celery import *
from celery import shared_task
from .models import *
import random

@shared_task
def do_smth():
    print('hello')

@app.task
def alter_prices():
    queryset = Commodity.objects.all()
    for cmd in queryset:
        cmd.price = cmd.get_new_price()
        cmd.save(update_fields=['price'])
