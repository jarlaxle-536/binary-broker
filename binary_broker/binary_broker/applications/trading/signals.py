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
    transaction = Transaction.objects.create(
        amount=-bet.venture, **{
        k: v for k, v in bet.__dict__.items()
        if k in ('owner', 'account_type')}
    )
    print(f'will sleep for {bet.duration} seconds.')
    time.sleep(bet.duration)
    bet.finalize_by_time()

@receiver(pre_save, sender=Transaction)
def transaction_pre_save_handler(sender, **kwargs):
    transaction = kwargs.get('instance', None)
    account = transaction.account
    new_account_havings = account.havings + transaction.amount
    if new_account_havings < 0:
        error_string = f"""
            Trying to yield transaction for amount bigger than account.havings:
            {account}, {transaction.amount}.
            """
        raise ValidationError(error_string)
    else:
        account.havings = new_account_havings
        account.save()

SIGNALS = [
    bet_post_save_handler,
    transaction_pre_save_handler
]
