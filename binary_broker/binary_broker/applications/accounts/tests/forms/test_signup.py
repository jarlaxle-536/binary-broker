from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

from binary_broker.applications.accounts.tests.fixtures.fixture_loader import *
from binary_broker.applications.accounts.forms import SignUpForm
from binary_broker.applications.accounts.models import *

class SignupFormTest(TestCase):

    def setUp(self):
        self.user_data = {
            'email': fixtures['email']['match'],
            'password': fixtures['password']['match']
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        self.signup_form = bs_object.find(
            'div', {'id': SIGNUP_FORM_DIV_ID}).find('form')

    def build_data(self, chosen):
        data = dict()
        for k, v in chosen.items():
            key = 'password' if k.startswith('password') else 'email'
            data[k] = fixtures[key][v]
        return data

    def general_test(self, chosen):
        data = self.build_data(chosen)
        bound_form = SignUpForm(data=data)
        error_codes = {k: [dct['code'] for dct in v]
            for k, v in json.loads(bound_form.errors.as_json()).items()}
        for k, v in chosen.items():
            for error_code in ERROR_CODES[k][v]:
                self.assertIn(error_code, error_codes.get(k, list()))

    def test_target(self):
        "Signup form => signup:POST, for old non-AJAX submit"
        self.assertEquals(self.signup_form.get('action'), reverse('signup'))
        self.assertEquals(self.signup_form.get('method'), 'post')

    def test_invalid_email(self):
        self.general_test({
            'email': 'invalid',
            'password': 'no_match'
        })

    def test_no_match_email(self):
        self.general_test({
            'email': 'no_match',
            'password': 'no_match'
        })

    def test_match_email(self):
        self.general_test({
            'email': 'match',
            'password': 'no_match'
        })

    def test_empty_password(self):
        self.general_test({
            'email': 'no_match',
            'password': 'empty'
        })

    def test_too_short_password(self):
        self.general_test({
            'email': 'no_match',
            'password': 'too_short'
        })

    def test_passwords_not_same(self):
        all_chosen = [{
            'email': 'no_match',
            'password': pw,
            'password_confirmation': pwc
        } for pw in VALID_PASSWORDS for pwc in VALID_PASSWORDS if pw != pwc]
        for chosen in all_chosen:
            data = self.build_data(chosen)
            bound_form = SignUpForm(data=data)
            error_codes = {k: [dct['code'] for dct in v]
                for k, v in json.loads(bound_form.errors.as_json()).items()}
            self.assertIn('passwords_do_not_match',
                error_codes.get('password_confirmation', []))

    def test_all_correct(self):
        all_chosen = [{
            'email': 'no_match',
            'password': pw,
            'password_confirmation': pw
        } for pw in VALID_PASSWORDS]
        for chosen in all_chosen:
            data = self.build_data(chosen)
            bound_form = SignUpForm(data=data)
            error_codes = {k: [dct['code'] for dct in v]
                for k, v in json.loads(bound_form.errors.as_json()).items()}
            self.assertEquals(error_codes, dict())

SIGNUP_FORM_DIV_ID = 'signup_form'
USER_DATA = {
    'email': fixtures['email']['no_match'],
    'password': fixtures['password']['no_match'],
    'password_confirmation': fixtures['password']['no_match']
}
ERROR_CODES = {
    'email': {
        'invalid':
            ['invalid'],
        'no_match':
            [],
        'match':
            ['unique']
    },
    'password': {
        'empty':
            ['required'],
        'too_short':
            ['password_too_short', 'password_too_common', 'password_entirely_numeric'],
        'no_match':
            [],
        'match':
            []
    }
}
ERROR_CODES['password_confirmation'] = ERROR_CODES['password']
VALID_PASSWORDS = ['no_match', 'match']
