from django.db import models
from simple_history.models import HistoricalRecords
import datetime
import random

from binary_broker.applications.accounts.models import CustomUser

class TimedeltaField(models.IntegerField):
    def __str__(self):
        return str(datetime.timedelta(seconds=self))

class Commodity(models.Model):

    DEFAULT_PRICE = 10.0

    class Meta:
        verbose_name_plural = 'commodities'

    name = models.CharField(max_length=50)
    mean_price = models.DecimalField(default=DEFAULT_PRICE, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=DEFAULT_PRICE, max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def get_new_price(self):
        return self.price + 0.05 * random.choice([-1, 1])

    def get_price_history(self):
        history_entries = self.history.all().order_by('history_date')
        price_history = [(e.history_date, e.price) for e in history_entries]
        return price_history

    def __str__(self):
        return f'{self.name}: {self.price} $'

class Bet(models.Model):

    DIRECTIONS = [(True, 'up'), (False, 'down')]
    DURATIONS = [(v, str(v))
        for v in [10, 30, 60, 120]]
    VENTURES = [(v, str(v))
        for v in [1, 2, 5, 10, 20, 50, 100]]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    direction = models.BooleanField(choices=DIRECTIONS, null=True)
    venture = models.DecimalField(choices=VENTURES, max_digits=10, decimal_places=2, null=False)
    duration = TimedeltaField(choices=DURATIONS, null=False)
    time_start = models.TimeField(auto_now_add=True)

    def time_finish(self):
        return self.time_start + self.duration
