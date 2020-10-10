from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from .exceptions import *
from .models import *

def user_does_not_exist_validator(value):
    try:
        CustomUser.objects.get(email=value)
    except ObjectDoesNotExist as exc:
        raise NoSuchUserError()

def user_already_exists_validator(value):
    try:
        CustomUser.objects.get(email=value)
        raise UserAlreadyExistsError()
    except ObjectDoesNotExist as exc:
        pass
