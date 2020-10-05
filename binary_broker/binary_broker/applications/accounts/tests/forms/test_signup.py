from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

from binary_broker.applications.accounts.forms import SignUpForm
from binary_broker.applications.accounts.models import *
from .fixture_loader import *

class SignupFormTest(TestCase):

    def setUp(self):
        self.user_data = {
            'email': emails['match'],
            'password': passwords['match']
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        self.signup_form = bs_object.find(
            'div', {'id': SIGNUP_FORM_DIV_ID}).find('form')

    def test_target(self):
        "Signup form => signup:POST, for old non-AJAX submit"
        self.assertEquals(self.signup_form.get('action'), reverse('signup'))
        self.assertEquals(self.signup_form.get('method'), 'post')

    def test_emails(self):
        "Provided password causes no errors, verify EMAIL"
        data = USER_DATA.copy()
        for email_k, email_v in emails.items():
            data['email'], errors = email_v, EMAIL_ERRORS[email_k]
            signup_data = {f'signup_{k}': v for k, v in data.items()}
            bound_form = SignUpForm(data=data)
            self.assertEquals(bound_form.is_valid(), not errors)
            for error in errors:
                self.assertIn(error, str(bound_form))

    def test_passwords(self):
        "Provided email causes no errors, verify PASSWORD"
        data = USER_DATA.copy()
        for pw_k, pw_v in passwords.items():
            data['password'], errors = pw_v, PASSWORD_ERRORS[pw_k]
            bound_form = SignUpForm(data=data)
            self.assertEquals(bound_form.is_valid(), not errors)
            if data['password'] != data['password_confirmation']:
                self.assertIn('Passwords do not match', str(bound_form))
            for error in errors:
                self.assertIn(error, str(bound_form))

SIGNUP_FORM_DIV_ID = 'signup_form'
EMAIL_ERRORS = {
    'invalid': ['Enter a valid email address.'],
    'no_match': [],
    'match': ['Custom user with this Email already exists.']
}
PASSWORD_ERRORS = {
    'empty': ['This field is required.'],
    'too_short': ['This password is too short.'],
    'no_match': [],
    'match': ['']
}
USER_DATA = {
    'email': emails['no_match'],
    'password': passwords['no_match'],
    'password_confirmation': passwords['no_match']
}
