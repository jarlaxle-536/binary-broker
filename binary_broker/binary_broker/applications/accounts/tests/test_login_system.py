from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class LoginSystemTest(TestCase):

    def test_login_form(self):
        "Login form => login:post"
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        login_form = bs_object.find(
            'div', {'id': LOGIN_FORM_DIV_ID}).find('form')
        self.assertEquals(login_form.get('action'), reverse('login'))
        self.assertEquals(login_form.get('method'), 'post')

LOGIN_FORM_DIV_ID = 'login_form'
