import random

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django_countries.fields import CountryField
from django.conf import settings
from django.db import models

from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_bot = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Bot(CustomUser):

    class Meta:
        proxy = True

class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    selected_account_type = models.CharField(
        max_length=20,
        choices=settings.PROFILE_ACCOUNT_TYPES,
        default=settings.PROFILE_ACCOUNT_TYPES[0][0],
        null=False
    )

    @property
    def current_account(self):
        return getattr(self,
            PROFILE_ACCOUNT_TYPE_RELATED_NAMES[self.selected_account_type])

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
        related_name=settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES['Demo']
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
        related_name=settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES['Real']
    )
    havings = models.DecimalField(
        **CashAccount.havings_settings,
        default=0
    )

    def __str__(self):
        return f'Real: {self.havings} $'
