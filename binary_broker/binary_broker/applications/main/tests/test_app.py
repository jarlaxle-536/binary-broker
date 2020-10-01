from django.urls import get_resolver
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class AppTest(TestCase):

    def test_app_pages(self):
        """will fail if no reverse is found (stuff_detail f.i.)"""
        paths = [p for p in get_resolver().reverse_dict.keys()
            if type(p) == str]
        for path in paths:
            response = self.client.get(reverse(path))
            self.assertEqual(response.status_code, 200)
