from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django import forms

from .validators import *

class LoginEmailField(forms.Field):

    default_validators = [
        validators.EmailValidator(
            message=_('EnterValidEmail')
        ),
        user_does_not_exist_validator
    ]

class SignupEmailField(forms.Field):

    default_validators = [
        validators.EmailValidator(
            message=_('EnterValidEmail')
        ),
        user_already_exists_validator
    ]

class PasswordField(forms.Field):

    default_validators = [
        validate_password,
    ]
