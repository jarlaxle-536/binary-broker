from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

def verbose(func):
    def wrapper(*args, **kwargs):
        print(func.__name__.upper())
        return func(*args, **kwargs)
    return wrapper

class CustomUserCreationTest(TestCase):

    name = 'creating general user'

    @verbose
    def test_create_user_with_no_email(self):
        fixture = build_fixture({
            'name': 'vasya',
            'password': None
            })
        with self.assertRaises(EmailNotProvided):
            CustomUser.objects.create_user(**fixture)

    @verbose
    def test_create_user_with_no_password(self):
        fixture = build_fixture({
            'email': None
            })
        with self.assertRaises(PasswordNotProvided):
            CustomUser.objects.create_user(**fixture)

    @verbose
    def test_create_user_with_invalid_email(self):
        fixture = build_fixture({
            'email': 'vasya',
            'password': None
            })
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(**fixture)

    @verbose
    def test_create_user_with_invalid_password(self):
        fixture = build_fixture({
            'email': None,
            'password': '1111'
        })
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(**fixture)

    @verbose
    def test_create_user_with_valid_email_and_password(self):
        fixture = build_fixture({
            'email': None,
            'password': None
        })
        CustomUser.objects.create_user(**fixture)

def build_fixture(dct):
    print(f'Building fixture from {dct}')
    fixture = {k: v if v else valid_fixture.get(k, None) for k, v in dct.items()}
    print(f'Created fixture: {fixture}')
    return fixture

FAKER = faker.Faker()
valid_fixture = {
    'email': FAKER.email(),
    'password': FAKER.password()
}
