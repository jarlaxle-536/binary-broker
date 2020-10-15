from django.core.exceptions import ValidationError

def validate_not_empty(value):
    if value == '':
        raise ValidationError(f'{value} is empty!')
