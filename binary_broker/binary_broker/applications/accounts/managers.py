from django.contrib.auth.base_user import BaseUserManager

from .exceptions import *

class UserManager(BaseUserManager):

    def create_user(self, *args, **kwargs):
        print(f'trying to create user with {args}, {kwargs}.')
        acquired_info = {k: kwargs.get(k, None) for k in ['email']}
        if acquired_info['email'] is None:
            raise EmailNotProvided
