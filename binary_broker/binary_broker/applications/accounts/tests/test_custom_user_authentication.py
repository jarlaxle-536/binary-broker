from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import faker

from binary_broker.applications.accounts.models import CustomUser
from binary_broker.applications.accounts.exceptions import *

class CustomUserAuthTest(TestCase):

    def setUp(self):
        print('setting up')
        for info in users:
            print(info['email'])
            user = CustomUser.objects.create_user(**info)
            print('user', user)

    def test_1(self):
        pass


FAKER = faker.Faker()

users = [
    {
        'email': FAKER.email(),
        'password': FAKER.password(),
        'is_superuser': False,
    },
    {
        'email': FAKER.email(),
        'password': FAKER.password(),
        'is_superuser': True
    }
]

print(users)
