from django.utils.translation import gettext_lazy as _
from django import forms

from .models import CustomUser

class LoginForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        labels = {
            'email': _('EmailString'),
            'password': _('Password')
        }

class SignUpForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField()
    password_confirmation = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation')
        labels = {
            'email': _('EmailString'),
            'password': _('Password'),
            'password_confirmation': _('PasswordConfirmation')
        }


    def clean(self):
#        print(self.__dict__)
        cleaned_data = super(SignUpForm, self).clean()
        passwords_match = len(set([cleaned_data.get(k)
            for k in ('password', 'password_confirmation')])) == 1
        if not passwords_match:
            raise forms.ValidationError('passwords do not match')
        return cleaned_data
