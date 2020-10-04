from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
import faker

from binary_broker.applications.accounts.models import *

class LoginViewTest(TestCase):

    def setUp(self):
        self.user_data = get_user_data()
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_login_view_post_match(self):
        "Login:post with user match"
        self.assertEquals(get_user(self.client), AnonymousUser())
        response = self.client.post(reverse('login'), data=self.user_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(get_user(self.client), self.user)

    def test_login_view_post_no_match(self):
        "Login:post with no user match"
        self.assertEquals(get_user(self.client), AnonymousUser())
        response = self.client.post(reverse('login'), data=get_user_data())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(get_user(self.client), AnonymousUser())

    """to do: tests on redirects to LOGIN_TARGET_URL"""

def get_user_data():
    return {'email': FAKER.email(), 'password': FAKER.password()}

FAKER = faker.Faker()
USER_DATA = get_user_data()
