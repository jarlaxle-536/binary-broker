from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from .exceptions import *

class UserManager(BaseUserManager):

    def _create_general_user(self, email=None, password=None, **extra_fields):
        print(f'Creating general user with email={email} and pw={password}')
        email = self.check_email(email)
        password = self.check_password(password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        print(user.__dict__)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_general_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_general_user(email, password, **extra_fields)

    def check_email(self, email):
        if email is None:
            raise EmailNotProvided
        validate_email(email)
        return self.normalize_email(email)

    def check_password(self, password):
        if password is None:
            raise PasswordNotProvided
        validate_password(password)
        return password
