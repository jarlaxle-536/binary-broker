from django.utils.translation import gettext_lazy as _
from django import forms

from .models import *

class BetFormPartial(forms.ModelForm):

    class Meta:
        model = Bet
        fields = ('venture', 'duration')

class BetFormFull(forms.ModelForm):

    class Meta:
        model = Bet
        fields = ('venture', 'duration', 'direction', 'owner', 'commodity', 'is_real_account')
