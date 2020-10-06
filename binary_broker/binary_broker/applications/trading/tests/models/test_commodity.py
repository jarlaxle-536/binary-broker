from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
import contextlib
import faker

from binary_broker.applications.trading.models import *

class CommodityTest(TestCase):

    """Testing Commodity model"""

    def test_create_some(self):
        cmd = Commodity.objects.create(name='horns_and_hooves')
