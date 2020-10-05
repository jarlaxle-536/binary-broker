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
    chosen_account = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default=ACCOUNT_TYPES[0],
        null=False
    )

    @classmethod
    def get_account_choice(cls, val):
        return [a for a in cls.ACCOUNT_TYPES if a[0] == val][0]

class DemoCashAccount(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='demo_account'
    )
    havings = models.FloatField(default=1000)

    def __str__(self):
        return f'Demo account: {self.havings} $'

class RealCashAccount(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='real_account'
    )
    havings = models.FloatField(default=0)

    def __str__(self):
        return f'Real account: {self.havings} $'
