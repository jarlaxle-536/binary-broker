from django.core.exceptions import ValidationError

from .exceptions import *

def validate_not_empty(value):
    if value == '':
        raise ValidationError(f'{value} is empty!')

def validate_sufficient_havings(account, amount):
    new_havings = account.havings + amount
    if new_havings < 0:
        error_string = 'Unable to yield transaction with amount > than account.havings.'
        raise NotSufficientHavings(error_string)
