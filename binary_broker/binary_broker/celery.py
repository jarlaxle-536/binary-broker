from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import datetime
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_broker.settings')
app = Celery('binary_broker')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'alter_prices': {
            'task': 'binary_broker.applications.trading.tasks.alter_prices',
            'schedule': datetime.timedelta(seconds=5)
        },
    }
)
