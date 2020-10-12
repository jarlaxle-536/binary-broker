from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
import datetime
import decimal
import random
import pytz

from binary_broker.applications.accounts.models import *

DEFAULT_NUMERIC_SETTINGS = {
    'max_digits': 10,
    'decimal_places': 2
}

class Commodity(models.Model):

    class Meta:
        verbose_name_plural = 'commodities'

    name = models.CharField(max_length=50)
    mean_price = models.DecimalField(default=10, **DEFAULT_NUMERIC_SETTINGS)
    price = models.DecimalField(default=10, **DEFAULT_NUMERIC_SETTINGS)
    history = HistoricalRecords()

    def get_new_price(self):
        max_dev = 0.01 * float(self.price)
        change = decimal.Decimal(2 * (random.random() - 0.5) * max_dev)
        self._diff = change
        print(self._diff, self.diff)
        return self.price + change

    @property
    def diff(self):
        return getattr(self, '_diff', 0)

    def get_price_history(self):
        history_entries = self.history.all().order_by('history_date')
        price_history = [(e.history_date, e.price) for e in history_entries]
        return price_history

    def get_last_records(self, timedelta):
        utc = pytz.UTC
        all_historical_entries = self.get_price_history()
        current_time = utc.localize(datetime.datetime.utcnow())
        min_time = current_time - timedelta
        for ind in range(len(all_historical_entries)):
            if all_historical_entries[ind][0] >= min_time: break
        last_entries = list(map(list, all_historical_entries[ind:]))
        last_entries[-1][0] =min_time
        while True:
            last = list(last_entries[-1])
            last[0] += settings.GLOBAL_UPDATE_PERIOD
            if last[0] >= current_time: break
            last_entries += [last[:]]
        return last_entries

    def __str__(self):
        return f'{self.name}: {self.price}'

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
    duration = models.IntegerField(choices=DURATIONS, null=False)
    time_start = models.TimeField(auto_now_add=True)

    def time_finish(self):
        return self.time_start + self.duration

    @property
    def account(self):
        profile = self.owner
        return getattr(profile, 'real_account' if self.is_real_account
            else 'demo_account')
