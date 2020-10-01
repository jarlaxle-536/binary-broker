from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from .exceptions import *

class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **info):
        print(email, password)
        email = self.check_email(email)
        password = self.check_password(password)
        user = self.model(email=email)
        user.set_password(password)
        print(user.__dict__)
        user.save()

    def check_email(self, email):
        if email is None:
            raise EmailNotProvided
        validate_email(email)
        return self.normalize_email(email)

    def check_password(self, password):
        if password is None:
            raise PasswordNotProvided
        validate_password(password)
        return
