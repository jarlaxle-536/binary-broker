from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

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

    def test_target(self):
        "Login form => login:POST, for old non-AJAX submit"
        self.assertEquals(self.login_form.get('action'), reverse('login'))
        self.assertEquals(self.login_form.get('method'), 'post')

    def test_emails(self):
        "Provided password causes no errors, verify EMAIL"
        data = self.user_data.copy()
        for email_k, email_v in emails.items():
            data['email'], errors = email_v, EMAIL_ERRORS[email_k]
            bound_form = LoginForm(data=data)
            self.assertEquals(bound_form.is_valid(), not errors)
            for error in errors:
                self.assertIn(error, str(bound_form))

    def test_passwords(self):
        "Provided email causes no errors, verify PASSWORD"
        data = self.user_data.copy()
        for pw_k, pw_v in passwords.items():
            data['password'], errors = pw_v, PASSWORD_ERRORS[pw_k]
            bound_form = LoginForm(data=data)
            self.assertEquals(bound_form.is_valid(), not errors)
            for error in errors:
                self.assertIn(error, str(bound_form))

LOGIN_FORM_DIV_ID = 'login_form'
EMAIL_ERRORS = {
    'invalid': ['Enter a valid email address.'],
    'no_match': [],
    'match': []
}
PASSWORD_ERRORS = {
    'empty': ['This field is required.'],
    'too_short': ['This password is too short.'],
    'no_match': [],
    'match': []
}
USER_DATA = {
    'email': emails['match'],
    'password': passwords['match']
}
