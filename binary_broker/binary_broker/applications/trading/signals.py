import time

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .exceptions import *
from .models import *

@receiver(post_save, sender=Bet)
def bet_post_save_handler(sender, **kwargs):
    bet = kwargs.get('instance', None)
    created = kwargs.get('created', None)
    if not created:
        return
    transaction = Transaction.objects.create(amount=-bet.venture, **{
        k: getattr(bet, k) for k in ('owner', 'account_type')}
    )

SIGNALS = [
#    bet_post_save_handler,
]
