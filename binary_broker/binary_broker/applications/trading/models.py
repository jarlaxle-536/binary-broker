from django.db import models
from simple_history.models import HistoricalRecords
import datetime
import decimal
import random

from binary_broker.applications.accounts.models import *

DEFAULT_NUMERIC_SETTINGS = {
    'max_digits': 10,
    'decimal_places': 2
}


class TimedeltaField(models.IntegerField):
    def __str__(self):
        return str(datetime.timedelta(seconds=self))

class Commodity(models.Model):

    class Meta:
        verbose_name_plural = 'commodities'

    name = models.CharField(max_length=50)
    mean_price = models.DecimalField(default=10, **DEFAULT_NUMERIC_SETTINGS)
    price = models.DecimalField(default=10, **DEFAULT_NUMERIC_SETTINGS)
    history = HistoricalRecords()

    def get_new_price(self):
        return self.price + decimal.Decimal(0.05 * random.choice([-1, 1]))

    def get_price_history(self):
        history_entries = self.history.all().order_by('history_date')
        price_history = [(e.history_date, e.price) for e in history_entries]
        return price_history

    def __str__(self):
        return f'{self.name}: {self.price} $'

class Bet(models.Model):

    DIRECTIONS = [(True, 'up'), (False, 'down')]
    IS_REAL = [(True, 'yes'), (False, 'no')]
    DURATIONS = [(v, str(v)) for v in [10, 30, 60, 120]]
    VENTURES = [(v, str(v)) for v in [1, 2, 5, 10, 20, 50, 100]]

    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_real_account = models.BooleanField(
        choices=IS_REAL,
        null=True,
        default=False
    )
    direction = models.BooleanField(choices=DIRECTIONS, null=True)
    venture = models.DecimalField(
        choices=VENTURES,
        null=False,
        **DEFAULT_NUMERIC_SETTINGS
    )
    duration = TimedeltaField(choices=DURATIONS, null=False)
    time_start = models.TimeField(auto_now_add=True)

    def time_finish(self):
        return self.time_start + self.duration

    @property
    def account(self):
        profile = self.owner
        return getattr(profile, 'real_account' if self.is_real_account
            else 'demo_account')
