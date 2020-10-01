from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

class CustomUserTest(TestCase):

    name = 'creating general user'

    def test_create_user_with_no_email(self):
        fixture = build_fixture({
            'name': 'vasya',
            'password': None
            })
        with self.assertRaises(EmailNotProvided):
            CustomUser.objects.create_user(**fixture)

    def test_create_user_with_no_password(self):
        fixture = build_fixture({
            'email': None
            })
        with self.assertRaises(PasswordNotProvided):
            CustomUser.objects.create_user(**fixture)

    def test_create_user_with_invalid_email(self):
        fixture = build_fixture({
            'email': 'vasya',
            'password': None
            })
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(**fixture)

    def test_create_user_with_invalid_password(self):
        fixture = build_fixture({
            'email': None,
            'password': '1111'
        })
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(**fixture)

    def test_create_user_with_valid_email_and_password(self):
        fixture = build_fixture({
            'email': None,
            'password': None
        })
        CustomUser.objects.create_user(**fixture)

def build_fixture(dct):
    res = {k: v if v else valid_fixture.get(k, None) for k, v in dct.items()}
    return res

FAKER = faker.Faker()
valid_fixture = {
    'email': 'vasya@google.com',
    'password': FAKER.password()
}
