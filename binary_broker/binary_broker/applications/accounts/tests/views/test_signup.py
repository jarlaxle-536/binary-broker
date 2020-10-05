from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
import faker

from binary_broker.applications.accounts.models import *

class LoginViewTest(TestCase):

    def setUp(self):
        self.user_data = get_user_data()
        self.user = CustomUser.objects.create_user(**{
            k: v for k, v in self.user_data.items()
            if k in ('email', 'password')
        })

    def test_signup_view_post_match(self):
        "Signup:post with user match"
        self.assertEquals(get_user(self.client), AnonymousUser())
        response = self.client.post(reverse('signup'), data=self.user_data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(get_user(self.client), AnonymousUser())

    def test_signup_view_post_no_match(self):
        "Signup:post with no user match"
        self.assertEquals(get_user(self.client), AnonymousUser())
        response = self.client.post(reverse('signup'), data=get_user_data(), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(get_user(self.client), AnonymousUser())

    """to do: tests on redirects to LOGIN_TARGET_URL"""

def get_user_data():
    dct = {'email': FAKER.email(), 'password': FAKER.password()}
    dct['password_confirmation'] = dct['password']
    return dct

FAKER = faker.Faker()
USER_DATA = get_user_data()
