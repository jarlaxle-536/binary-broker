from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import *

@receiver(pre_save, sender=Bet)
def bet_creation_handler(sender, **kwargs):
    bet = kwargs.get('instance', None)
    print(f'{bet} pre save')
    if bet.venture > bet.account.havings:
        print('error here, this faggot is trying to make a bet with venture bigger than his account havings')
        raise Exception('wtf dude')
    else:
        bet.account.havings -= bet.venture

SIGNALS = [
    bet_creation_handler,
]
