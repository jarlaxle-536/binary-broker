from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class EmailNotProvided(Exception):
    pass

class PasswordNotProvided(Exception):
    pass

class GeneralValidationError(ValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(self.message, code=self.code)

class NoSuchUserError(GeneralValidationError):
    message = _('NoSuchUser')
    code = 'no_such_user'

class IncorrectPasswordError(GeneralValidationError):
    message = _('PasswordIncorrect')
    code = 'incorrect_password'

class UserAlreadyExistsError(GeneralValidationError):
    message = _('UserAlreadyExists')
    code = 'unique'

class PasswordsDoNotMatch(GeneralValidationError):
    message = _('PasswordsDoNotMatch')
    code = 'passwords_do_not_match'
