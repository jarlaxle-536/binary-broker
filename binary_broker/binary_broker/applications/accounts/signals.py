from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=CustomUser)
def profile_creation_handler(sender, **kwargs):
    user = kwargs.get('instance', None)
    profile = Profile.objects.create(user=user)

SIGNALS = [
    profile_creation_handler,
]