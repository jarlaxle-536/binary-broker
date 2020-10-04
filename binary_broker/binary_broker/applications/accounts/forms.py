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

    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_password]
        print(kwargs)
        super().__init__(*args, **kwargs)

    def validate(self, value):
        print(f'validating {self} with {value}.')
        try:
            validate_password(value)
        except ValidationError as exc:
            res = ValidationError(exc)
            print(res)
            raise res

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField()
    password_confirmation = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation')

    def clean(self):
#        print(self.__dict__)
        cleaned_data = super(SignUpForm, self).clean()
        passwords_match = len(set([cleaned_data.get(k)
            for k in ('password', 'password_confirmation')])) == 1
        if not passwords_match:
            raise forms.ValidationError('passwords do not match')
        return cleaned_data
