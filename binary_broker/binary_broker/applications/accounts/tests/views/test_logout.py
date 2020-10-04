from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
import faker

from binary_broker.applications.accounts.models import *

class LogoutViewTest(TestCase):

    def setUp(self):
        self.user_data = get_user_data()
        self.user = CustomUser.objects.create_user(**{
            k: v for k, v in self.user_data.items()
            if k in ('email', 'password')
        })
        self.client.post(reverse('login'), data=self.user_data)

    def test_logout_view_get(self):
        "Logout:get"
        self.assertEquals(get_user(self.client), self.user)
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(get_user(self.client), AnonymousUser())

    """to do: tests on redirects to LOGIN_TARGET_URL"""

def get_user_data():
    dct = {'email': FAKER.email(), 'password': FAKER.password()}
    dct['password_confirmation'] = dct['password']
    return dct

FAKER = faker.Faker()
USER_DATA = get_user_data()
