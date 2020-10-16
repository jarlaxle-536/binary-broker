from django.utils.translation import gettext_lazy as _
from django import forms

from .models import *

class BetForm(forms.ModelForm):

    class Meta:
        model = Bet
        fields = (
            'venture',
            'duration',
            'direction_up',
            'owner',
            'asset',
            'account_type'
        )

class PartialBetForm(BetForm):
    class Meta:
        model = Bet
        fields = ('venture', 'duration')
