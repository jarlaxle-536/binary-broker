from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import contextlib
import faker

from binary_broker.applications.trading.models import *
from binary_broker.applications.accounts.models import *

class BetTest(TestCase):

    """Testing Bet model"""

    def setUp(self):
        self.commodity = Commodity.objects.create(name='horns_and_hooves')
        self.user = CustomUser.objects.create_user(
            email=FAKER.email(),
            password=FAKER.password()
        )
        self.default_bet_settings = {
            'commodity': self.commodity,
            'owner': self.user.profile,
            'direction': True,
            'venture': 1,
            'duration': 10
        }

    def test_create_some(self):
        demo_bet = Bet.objects.create(**self.default_bet_settings)
        self.assertEquals(demo_bet.account, self.user.profile.demo_account)
        real_bet = Bet.objects.create(
            is_real_account=True,
            **self.default_bet_settings
        )
        self.assertEquals(real_bet.account, self.user.profile.real_account)

FAKER = faker.Faker()
