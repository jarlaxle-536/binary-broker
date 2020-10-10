from django.utils.translation import gettext_lazy as _
from django import forms

from .form_fields import *
from .exceptions import *
from .models import *

class LoginForm(forms.Form):

    email = LoginEmailField(
        label=_('Email')
    )
    password = PasswordField(
        label=_('Password')
    )

    def clean(self):
        super().clean()
        if all(map(lambda f: f in self.cleaned_data, self.fields)):
            user = CustomUser.objects.get(email=self.cleaned_data['email'])
            if not user.check_password(self.cleaned_data['password']):
                self.add_error('password', IncorrectPasswordError())
        return self.cleaned_data

class SignUpForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    email = SignupEmailField(
        label=_('Email')
    )
    password = PasswordField(
        label=_('Password')
    )
    password_confirmation = PasswordField(
        label=_('Password confirmation')
    )

    def clean(self):
        super().clean()
        if all(map(lambda f: f in self.cleaned_data, self.fields)):
            if len(set([v for k, v in self.cleaned_data.items()
                if k.startswith('password')])) != 1:
                self.add_error('password_confirmation',
                    PasswordsDoNotMatch())
        return self.cleaned_data

class ProfileAccountTypeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('chosen_account', )
