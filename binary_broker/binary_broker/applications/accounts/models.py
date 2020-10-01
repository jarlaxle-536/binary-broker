from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
