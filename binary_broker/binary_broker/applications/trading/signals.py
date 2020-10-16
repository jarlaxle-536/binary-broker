import time

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .exceptions import *
from .models import *

@receiver(post_save, sender=Bet)
def bet_post_save_handler(sender, **kwargs):
    bet = kwargs.get('instance', None)
    created = kwargs.get('created', None)
    if not created: return
    if bet.venture > bet.account.havings:
        raise VentureBiggerThanAccountHavings('')
    else:
        bet.account.havings -= bet.venture
        bet.account.save()
        print(f'will sleep for {bet.duration} seconds.')
        time.sleep(bet.duration)
        bet.finalize_by_time()

SIGNALS = [
    bet_post_save_handler,
]
