from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    ACCOUNT_TYPES = [(v, str(v)) for v in ['Demo', 'Real']]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    chosen_account = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)

class DemoCashAccount(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='demo_account'
    )
    havings = models.FloatField(default=1000)

class RealCashAccount(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='real_account'
    )
    havings = models.FloatField(default=0)
