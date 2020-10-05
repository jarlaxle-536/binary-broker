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

    def set_password(self, password):
        print('setting password')
        print('raw:', password)
        print('hashed:', self.password)
        super().set_password(password)

    def check_password(self, password):
        print('checking password')
        print('raw:', password)
        print('hashed:', self.password)
        return super().check_password(password)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
