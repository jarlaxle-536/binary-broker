import contextlib, datetime, faker, pytz

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, tag

from binary_broker.applications.trading.exceptions import *
from binary_broker.applications.accounts.models import *
from binary_broker.applications.trading.models import *

@tag('model', 'bet')
class BetTest(TestCase):

    """Testing Bet model"""

    def setUp(self):
        self.asset = Asset.objects.create(name='horns_and_hooves')
        self.user = CustomUser.objects.create_user(
            email=FAKER.email(),
            password=FAKER.password()
        )
        self.default_bet_settings = {
            'asset': self.asset,
            'owner': self.user.profile,
            'direction_up': True,
            'venture': 1,
            'duration': 10
        }

    def test_default_bet_settings(self):
        bet = Bet.objects.create(**self.default_bet_settings)
        for field, value in self.default_bet_settings.items():
            self.assertEquals(getattr(bet, field), value)

    def test_bet_asset(self):
        """
            test that bet.asset cannot be changed after creation
        """
        pass

    def test_bet_owner(self):
        """
            test that bet.owner cannot be changed after creation
        """
        pass

    def test_bet_direction_up(self):
        """
            test that bet.direction_up cannot be changed after creation
        """
        pass

    def test_bet_venture(self):
        """
            test that bet.venture cannot be changed after creation
        """
        pass

    def test_bet_time_start(self):
        """
            bet.time_start is DateTimeField with auto_now_add=True
        """
        utc = pytz.UTC
        current_time = utc.localize(datetime.datetime.utcnow())

        bet = Bet.objects.create(**self.default_bet_settings)
        time_diff = bet.time_start - current_time
        self.assertTrue(time_diff < datetime.timedelta(seconds=1))

    def test_bet_success(self):
        """
            bet.success is BooleanField, blank=null=True.
            Is recalculated on bet.finalize().
        """
        pass

    def test_bet_default_demo_account(self):
        bet = Bet.objects.create(**self.default_bet_settings)
        self.assertEquals(bet.account, self.user.profile.demo_account)
#        print('UP chosen acc:', self.user.profile.chosen_account)

    def not_test_bet_real_account_zero_havings(self):
        bet_settings = self.default_bet_settings.copy()
        bet_settings['is_real_account'] = True
        self.assertEquals()
        with self.assertRaises(VentureBiggerThanAccountHavings):
            bet = Bet.objects.create(**bet_settings)
#        self.assertEquals(bet.account, self.user.profile.real_account)

FAKER = faker.Faker()
