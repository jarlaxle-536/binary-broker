from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django import forms

from .models import CustomUser

def will_raise(value):
    print('i will raise')
    raise ValidationError('bla')

class PasswordField(forms.CharField):

    widget = forms.PasswordInput
    default_validators = [validate_password]

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as exc:
            self.add_error('password', exc)
        return password

class SignUpForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

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
