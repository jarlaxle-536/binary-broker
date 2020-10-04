from django.contrib.auth import authenticate
from django.test import TestCase
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

class CustomUserAuthTest(TestCase):

    def test_authenticate_general_user(self):
        """Authenticate GENERAL USER"""
        CustomUser.objects.create_user(**user_info)
        user = authenticate(**user_info)
        self.assertTrue(user.is_authenticated)

    def test_authenticate_superuser(self):
        """Authenticate SUPERUSER"""
        CustomUser.objects.create_superuser(**user_info)
        user = authenticate(**user_info)
        self.assertTrue(user.is_authenticated)

FAKER = faker.Faker()
user_info = {
        'email': FAKER.email(),
        'password': FAKER.password(),
    }
