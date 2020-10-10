from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
import json

from binary_broker.applications.accounts.models import *
from binary_broker.applications.accounts.forms import LoginForm
from .fixture_loader import *

class LoginFormTest(TestCase):

    def setUp(self):
        self.user_data = USER_DATA
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        self.login_form = bs_object.find(
            'div', {'id': LOGIN_FORM_DIV_ID}).find('form')

    def general_test(self, chosen):
        data = {k: fixtures[k][v] for k, v in chosen.items()}
        bound_form = LoginForm(data=data)
        error_codes = {k: [dct['code'] for dct in v]
            for k, v in json.loads(bound_form.errors.as_json()).items()}
        for k, v in chosen.items():
            for error_code in ERROR_CODES[k][v]:
                self.assertIn(error_code, error_codes.get(k, list()))

    def test_target(self):
        "Login form => login:POST, for old non-AJAX submit"
        self.assertEquals(self.login_form.get('action'), reverse('login'))
        self.assertEquals(self.login_form.get('method'), 'post')

    def test_invalid_email(self):
        self.general_test({
            'email': 'invalid',
            'password': 'match'
        })

    def test_no_match_email(self):
        self.general_test({
            'email': 'no_match',
            'password': 'match'
        })

    def test_empty_password(self):
        self.general_test({
            'email': 'match',
            'password': 'empty'
        })

    def test_too_short_password(self):
        self.general_test({
            'email': 'match',
            'password': 'too_short'
        })

    def test_incorrect_password(self):
        self.general_test({
            'email': 'match',
            'password': 'no_match'
        })

    def test_all_correct(self):
        self.general_test({
            'email': 'match',
            'password': 'match'
        })

LOGIN_FORM_DIV_ID = 'login_form'
USER_DATA = {
    'email': fixtures['email']['match'],
    'password': fixtures['password']['match']
}
ERROR_CODES = {
    'email': {
        'invalid':
            ['invalid'],
        'no_match':
            ['no_such_user'],
        'match':
            []
    },
    'password': {
        'empty':
            ['required'],
        'too_short':
            ['password_too_short', 'password_too_common', 'password_entirely_numeric'],
        'no_match':
            ['incorrect_password'],
        'match':
            []
    }
}
