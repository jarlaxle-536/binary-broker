from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class SignupSystemTest(TestCase):

    def test_signup_form(self):
        "Signup form => signup:post"
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        login_form = bs_object.find(
            'div', {'id': SIGNUP_FORM_DIV_ID}).find('form')
        self.assertEquals(login_form.get('action'), reverse('signup'))
        self.assertEquals(login_form.get('method'), 'post')

SIGNUP_FORM_DIV_ID = 'signup_form'
