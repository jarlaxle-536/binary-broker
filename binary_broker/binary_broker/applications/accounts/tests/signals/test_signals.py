from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import contextlib
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

class UserSignalsTest(TestCase):

    """Testing user signals"""

    def general_test(self,
            fixture={'email': None, 'password': None},
            func = CustomUser.objects.create_user,
            exception_catched=None,
            check_func=None):
        """Template for actual tests"""
        context_manager = (self.assertRaises(exception_catched)
            if exception_catched else contextlib.nullcontext())
        with context_manager:
            result = func(**build_fixture(fixture))
            print(result.__dict__)
            if check_func:
                check_func(result)

    def test_profile_created(self):
        """
            Profile is created with user creation.
        """
        self.general_test(
            fixture={'email': None, 'password': None},
            check_func=lambda result:
                self.assertEquals(result, result.profile.user),
        )

    def test_cash_accounts_created(self):
        """
            Accounts (demo and real) are created with profile creation.
        """
        self.general_test(
            fixture={'email': None, 'password': None},
            check_func=lambda result: (
                self.assertEquals(result.profile.demo_account.profile,
                    result.profile) and
                self.assertEquals(result.profile.real_account.profile,
                    result.profile)
            ),
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
