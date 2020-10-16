import datetime, decimal, random, pytz

from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models

from binary_broker.applications.accounts.models import *
from .validators import *

class Asset(models.Model):

    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        validators=[validate_not_empty]
    )
    mean_price = models.DecimalField(
        default=10,
        **settings.DEFAULT_NUMERIC_SETTINGS
    )
    price = models.DecimalField(
        default=10,
        **settings.DEFAULT_NUMERIC_SETTINGS
    )
    history = HistoricalRecords()

    def get_new_price(self):
        max_dev = 0.01 * float(self.price)
        change = decimal.Decimal(2 * (random.random() - 0.5) * max_dev)
        self._diff = change
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

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        null=False
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False
    )
    is_real_account = models.BooleanField(
        choices=settings.BET_IS_REAL,
        null=False,
        default=False
    )
    direction_up = models.BooleanField(
        choices=settings.BET_DIRECTIONS,
        null=False
    )
    venture = models.DecimalField(
        choices=settings.BET_VENTURES,
        null=False,
        **settings.DEFAULT_NUMERIC_SETTINGS
    )
    duration = models.IntegerField(
        choices=settings.BET_DURATIONS,
        null=False
    )
    time_start = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.price_when_created = self.asset.price

    @property
    def finalized(self):
        return getattr(self, '_finalized', False)

    @property
    def time_finish(self):
        return self.time_start + datetime.timedelta(seconds=self.duration)

    @property
    def account(self):
        profile = self.owner
        return getattr(profile, 'real_account' if self.is_real_account
            else 'demo_account')

    def finalize_by_time(self, time):
        print(f'Finalizing {self}.')
        print(f'Time: {time}')
        print(f'Finish time: {self.time_finish}')
        if self.time_finish > time or self.finalized: return
        print(f'{self} done')
        success = self.direction_up == (self.asset.price -
            self.price_when_created > 0)
        if success:
            print(f'{self} WON!')
            self.account.havings += 2 * self.venture
            self.account.save()
        else:
            print(f'{self} LOST!')
        self.success = success
        self._finalized = True
        self.save()
        print(self.__dict__)
