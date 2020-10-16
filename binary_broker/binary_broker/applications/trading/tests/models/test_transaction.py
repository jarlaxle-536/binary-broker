import contextlib, datetime, faker, pytz

from django.test import TestCase, TransactionTestCase, tag
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.conf import settings

from binary_broker.applications.trading.exceptions import *
from binary_broker.applications.accounts.models import *
from binary_broker.applications.trading.models import *

@tag('model', 'transaction')
class TransactionModelTest(TransactionTestCase):

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

    def test_transaction_successful(self):
        for acc_type, acc_rel_name in \
            settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES.items():
            default_transaction_settings = {
                'owner': self.user.profile,
                'account_type': acc_type,
            }
            account = getattr(self.user.profile, acc_rel_name)
            havings = account.havings
            amount = 0
            transaction = Transaction.objects.create(amount=amount,
                **default_transaction_settings)
            self.assertEqual(havings + amount, account.havings)

    def test_transaction_failed(self):
        for acc_type, acc_rel_name in \
            settings.PROFILE_ACCOUNT_TYPE_RELATED_NAMES.items():
            default_transaction_settings = {
                'owner': self.user.profile,
                'account_type': acc_type,
            }
            account = getattr(self.user.profile, acc_rel_name)
            havings = account.havings
            amount = -10 ** 6
            with self.assertRaises(NotSufficientHavings):
                transaction = Transaction.objects.create(amount=amount,
                    **default_transaction_settings)
            self.assertEqual(havings, account.havings)

    def test_transaction_is_created_with_bet(self):
        bet = Bet.objects.create(**self.default_bet_settings)
        transaction = Transaction.objects.last()
        self.assertEquals(
            - float(bet.venture),
            float(transaction.amount)
        )
        for field in ('owner', 'account'):
            self.assertEquals(
                getattr(bet, field), getattr(transaction, field))

    def test_no_transaction_no_bet(self):
        bet_settings = self.default_bet_settings.copy()
        bet_settings['venture'] = 10 ** 6
        prev_count = Bet.objects.count()
        'make sure no bet is created if transaction fails'
        with self.assertRaises(NotSufficientHavings):
            bet = Bet.objects.create(**bet_settings)
        self.assertEquals(Bet.objects.count(), prev_count)

FAKER = faker.Faker()
