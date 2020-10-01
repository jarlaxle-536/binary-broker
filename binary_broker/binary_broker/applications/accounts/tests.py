from django.test import TestCase
from django.db.utils import IntegrityError
import unittest

from .models import CustomUser
from .exceptions import *

class CustomUserTest(TestCase):

    name = 'testing custom user'

    def test_create_user_with_no_email(self):
        with self.assertRaises(EmailNotProvided):
            CustomUser.objects.create_user(name='Vasya')

    def test_create_user_with_email(self):
        CustomUser.objects.create_user(email='vasya_pupkin@google.com')
