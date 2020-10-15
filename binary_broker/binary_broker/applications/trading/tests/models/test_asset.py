from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, tag
import contextlib
import faker

from binary_broker.applications.trading.models import *

@tag('model')
class AssetTest(TestCase):

    """Testing Asset model"""

    def test_create_some(self):
        cmd = Asset.objects.create(name='horns_and_hooves')
