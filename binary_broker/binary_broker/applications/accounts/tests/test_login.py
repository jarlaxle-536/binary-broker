from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
import faker

from binary_broker.applications.accounts.models import *
from binary_broker.applications.accounts.forms import LoginForm

class LoginTest(TestCase):

    def setUp(self):
        print()
        print('SETUP')
        self.user_data = get_user_data()
        self.user = CustomUser.objects.create_user(**self.user_data)
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        self.login_form = bs_object.find(
            'div', {'id': LOGIN_FORM_DIV_ID}).find('form')

    def test_login_view_post_match(self):
        "Login:post with match"
        pass

def get_user_data():
    return {'email': FAKER.email(), 'password': FAKER.password()}

def create_query_dict(dct):
    query_dict = QueryDict('', mutable=True)
    query_dict.update(dct)
    return query_dict

LOGIN_FORM_DIV_ID = 'login_form'
FAKER = faker.Faker()
