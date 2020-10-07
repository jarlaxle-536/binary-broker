from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import datetime
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_broker.settings')
app = Celery('binary_broker')

app.config_from_object('django.conf:settings')
app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks()

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'alter_prices': {
            'task': 'binary_broker.applications.trading.tasks.alter_prices',
            'schedule': settings.GLOBAL_UPDATE_PERIOD
        },
        'update_trading': {
            'task': 'binary_broker.applications.trading.tasks.update_trading',
            'schedule': settings.GLOBAL_UPDATE_PERIOD
        },
    }
)
