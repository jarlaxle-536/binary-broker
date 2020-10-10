from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.core import validators
from django import forms

from .models import CustomUser, Profile
from .exceptions import *

class CustomEmailField(forms.Field):

    default_validators = [
        validators.EmailValidator(
            message=_('EnterValidEmail')
        ),
    ]

class LoginPasswordField(forms.Field):

    default_validators = [
        validate_password
    ]

class LoginForm(forms.Form):

    email = CustomEmailField(label=_('Email'))
    password = LoginPasswordField(label=_('Password'))

    def clean(self):
        super().clean()
        if all(map(lambda f: f in self.cleaned_data, self.fields)):
            try:
                user = CustomUser.objects.get(email=self.cleaned_data['email'])
                if not user.check_password(self.cleaned_data['password']):
                    self.add_error('password', IncorrectPasswordError())
            except ObjectDoesNotExist as exc:
                self.add_error('email', NoSuchUserError())
        return self.cleaned_data

class SignUpPasswordField(forms.CharField):

    default_validators = tuple()

class PasswordConfirmationField(forms.CharField):

    default_validators = tuple()

class SignUpForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    email = CustomEmailField(
        label=_('Email')
    )
    password = SignUpPasswordField(
        label=_('Password')
    )
    password_confirmation = PasswordConfirmationField(
        label=_('Password confirmation')
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        for field in ('password', 'password_confirmation'):
            value = cleaned_data.get(field)
            if value:
                try:
                    validate_password(cleaned_data.get(field))
                except ValidationError as exc:
                    self.add_error(field, exc)
        passwords_match = cleaned_data.get('password') == \
            cleaned_data.get('password_confirmation')
        if not passwords_match:
            raise forms.ValidationError('Passwords do not match.')
        cleaned_data.pop('password_confirmation', None)
        return cleaned_data

class ProfileAccountTypeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('chosen_account', )
