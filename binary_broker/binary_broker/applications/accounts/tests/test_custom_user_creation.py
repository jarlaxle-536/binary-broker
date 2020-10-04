from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import contextlib
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

class CustomUserCreationTest(TestCase):

    name = 'creating user tests'

    def general_test(self,
            fixture={'email': None, 'password': None},
            func = CustomUser.objects.create_user,
            exception_catched=None,
            check_func=None):
        context_manager = (self.assertRaises(exception_catched)
            if exception_catched else contextlib.nullcontext())
        with context_manager:
            result = func(**build_fixture(fixture))
            if check_func:
                check_func(result)

    def test_create_user_with_smth_missing(self):
        """Create user with smth missing"""
        self.general_test(
            fixture={'name': 'vasya', 'password': None},
            exception_catched=EmailNotProvided
        )
        self.general_test(
            fixture={'email': None},
            exception_catched=PasswordNotProvided
        )

    def test_create_user_with_smth_invalid(self):
        """Create user with smth invalid"""
        self.general_test(
            fixture={'email': 'vasya', 'password': None},
            exception_catched=ValidationError
        )
        self.general_test(
            fixture={'email': None, 'password': '1'},
            exception_catched=ValidationError
        )

    def test_create_valid_users(self):
        """Create user with everything valid"""
        self.general_test(
            fixture={'email': None, 'password': None}
        )
        self.general_test(
            fixture={'email': None, 'password': None},
            func=CustomUser.objects.create_superuser,
            check_func=lambda result: self.assertTrue(result.is_superuser),
        )

    def test_profile_created(self):
        """Profile is created with user creation"""
        self.general_test(
            fixture={'email': None, 'password': None},
            check_func=lambda result: self.assertEquals(result, result.profile.user),
        )

def build_fixture(dct):
    fixture = {k: v if v else valid_fixture.get(k, lambda: None).__call__()
        for k, v in dct.items()}
    return fixture

FAKER = faker.Faker()
valid_fixture = {
    'email': lambda : FAKER.email(),
    'password': lambda : FAKER.password()
}
