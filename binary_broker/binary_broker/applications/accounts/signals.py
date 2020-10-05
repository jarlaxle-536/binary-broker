from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=CustomUser)
def profile_creation_handler(sender, **kwargs):
    user = kwargs.get('instance', None)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.save()

@receiver(post_save, sender=Profile)
def accounts_creation_handler(sender, **kwargs):
    profile = kwargs.get('instance', None)
    demo_account, created = DemoCashAccount.objects.get_or_create(profile=profile)
    demo_account.save()
    real_account, create = RealCashAccount.objects.get_or_create(profile=profile)
    real_account.save()

SIGNALS = [
    profile_creation_handler,
    accounts_creation_handler
]
