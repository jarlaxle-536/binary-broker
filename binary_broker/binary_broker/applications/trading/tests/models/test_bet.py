import contextlib, datetime, faker, pytz

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase, tag
from django.db.utils import IntegrityError
from django.conf import settings

from binary_broker.applications.trading.exceptions import *
from binary_broker.applications.accounts.models import *
from binary_broker.applications.trading.models import *

@tag('model', 'bet')
class BetModelGeneralTest(TransactionTestCase):

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
            'venture': settings.BET_VENTURES[1][0],
            'duration': settings.BET_DURATIONS[0][0]
        }

    def test_bet_default_settings(self):
        bet = Bet.objects.create(**self.default_bet_settings)
        for field, value in self.default_bet_settings.items():
            self.assertEquals(getattr(bet, field), value)

    def test_bet_mandatory_fields(self):
        for field in settings.BET_MANDATORY_FIELDS:
            bet_info = self.default_bet_settings.copy()
            bet_info.pop(field, None)
            with self.assertRaises((
                IntegrityError, ObjectDoesNotExist, ValidationError)):
                bet = Bet.objects.create(**bet_info)

    def test_bet_time_start(self):
        utc = pytz.UTC
        current_time = utc.localize(datetime.datetime.utcnow())
        bet = Bet.objects.create(**self.default_bet_settings)
        time_diff = bet.time_start - current_time
        self.assertTrue(time_diff < datetime.timedelta(seconds=1))

    def test_bet_account(self):
        for acc_type, acc_rel_name in settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES.items():
            bet_settings = self.default_bet_settings.copy()
            self.user.profile.selected_account_type = acc_type
            'ensure any profile has sufficient havings to make a bet'
            self.user.profile.current_account.havings = self.default_bet_settings['venture']
            bet = Bet.objects.create(**bet_settings)
            bet_account = self.user.profile.current_account
            self.assertEquals(bet.account, bet_account)
            another_acc_type = [
                k for k in settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES
                if k != acc_type
            ][0]
            'ensure bet still points to the same account'
            self.user.profile.selected_account_type = another_acc_type
            self.assertEquals(bet.account, bet_account)

    def test_bet_default_demo_account(self):
        bet = Bet.objects.create(**self.default_bet_settings)
        self.assertEquals(bet.account, self.user.profile.demo_account)

FAKER = faker.Faker()
