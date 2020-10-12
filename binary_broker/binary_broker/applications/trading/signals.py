from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=Bet)
def bet_creation_handler(sender, **kwargs):
    bet = kwargs.get('instance', None)
    created = kwargs.get('created', None)
    print(f'calling {bet} post save, created={created}')
    if not created: return
    if bet.venture > bet.account.havings:
        print('error here, this faggot is trying to make a bet with venture bigger than his account havings')
        raise Exception('wtf dude')
    else:
        bet.account.havings -= bet.venture
        bet.account.save()

SIGNALS = [
    bet_creation_handler,
]
