from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
import faker

from binary_broker.applications.accounts.models import *
from binary_broker.applications.accounts.forms import LoginForm

class LoginFormTest(TestCase):

    def setUp(self):
        self.user_data = get_user_data()
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        self.login_form = bs_object.find(
            'div', {'id': LOGIN_FORM_DIV_ID}).find('form')

    def test_target(self):
        "Login form => login:post"
        self.assertEquals(self.login_form.get('action'), reverse('login'))
        self.assertEquals(self.login_form.get('method'), 'post')

    def test_email(self):
        "Provided password causes no errors, verify EMAIL"
        data = {'password': passwords['match']['value']}
        for email_k, email_v in emails.items():
            data['email'] = email_v['value']
            bound_form = LoginForm(data=data)
            is_email_valid = not email_v['errors']
            is_form_valid = bound_form.is_valid()
            self.assertEquals(is_form_valid, is_email_valid)
            for error in email_v['errors']:
                self.assertIn(error, str(bound_form))

    def test_password(self):
        "Provided email causes no errors, verify PASSWORD"
        data = {'email': emails['match']['value']}
        for pw_k, pw_v in passwords.items():
            data['password'] = pw_v['value']
            bound_form = LoginForm(data=data)
            is_password_valid = not pw_v['errors']
            is_form_valid = bound_form.is_valid()
            self.assertEquals(is_form_valid, is_password_valid)
            for error in pw_v['errors']:
                self.assertIn(error, str(bound_form))

def get_user_data():
    return {'email': FAKER.email(), 'password': FAKER.password()}

LOGIN_FORM_DIV_ID = 'login_form'

FAKER = faker.Faker()
USER_DATA = get_user_data()

emails = {
    'invalid': {
        'value': 'vasya',
        'errors': [
            'Enter a valid email address.'
        ]
    },
    'no_match': {
        'value': FAKER.email(),
        'errors': []
    },
    'match': {
        'value': USER_DATA['email'],
        'errors': []
    }
}

passwords = {
    'empty': {
        'value': '',
        'errors': [
            'This password is too short.'
        ]
    },
    'too_short': {
        'value': '1',
        'errors': [
            'This password is too short.'
        ]
    },
    'no_match': {
        'value': FAKER.password(),
        'errors': []
    },
    'match': {
        'value': USER_DATA['password'],
        'errors': []
    },
}
