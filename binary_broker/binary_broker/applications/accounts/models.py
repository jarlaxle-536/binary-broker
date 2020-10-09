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

    def __str__(self):
        return f'{self.user}'

class CashAccount(models.Model):

    profile_args, profile_kwargs = (Profile, ), {'on_delete': models.CASCADE}
    havings_settings = {'max_digits': 10, 'decimal_places': 2}

    class Meta:
        abstract = True

class DemoCashAccount(CashAccount):

    profile = models.OneToOneField(
        *CashAccount.profile_args,
        **CashAccount.profile_kwargs,
        related_name='demo_account'
    )
    havings = models.DecimalField(
        **CashAccount.havings_settings,
        default=1000
    )

    def __str__(self):
        return f'Demo: {self.havings} $'

class RealCashAccount(CashAccount):

    profile = models.OneToOneField(
        *CashAccount.profile_args,
        **CashAccount.profile_kwargs,
        related_name='real_account'
    )
    havings = models.DecimalField(
        **CashAccount.havings_settings,
        default=0
    )

    def __str__(self):
        return f'Real: {self.havings} $'
