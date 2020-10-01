import django.forms as dj_forms

from .models import User

class RegisterForm(dj_forms.ModelForm):
    email = dj_forms.EmailField()
    password = dj_forms.CharField()
    password_confirmation = dj_forms.CharField()

    class Meta:
        model = User
        fields = ["email", "password"]
