from django.test import TestCase, TransactionTestCase, tag
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import contextlib
import faker

from binary_broker.applications.trading.models import *

@tag('model', 'asset')
class AssetModelGeneralTest(TransactionTestCase):

    def setUp(self):
        self.default_asset_settings = {
            'name': 'horns_and_hooves',
        }

    def test_asset_default_settings(self):
        asset = Asset.objects.create(**self.default_asset_settings)
        for field, value in self.default_asset_settings.items():
            self.assertEquals(getattr(asset, field), value)

    def test_asset_has_at_least_one_historical_record(self):
        asset = Asset.objects.create(**self.default_asset_settings)
        self.assertTrue(asset.history.count() >= 1)
