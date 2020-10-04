from django.urls import get_resolver
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class AppTest(TestCase):

    def test_app_pages(self):
        """Test all app pages"""
        paths = [p for p in get_resolver().reverse_dict.keys()
            if type(p) == str]
        for path in paths:
            response = self.client.get(reverse(path))
            self.assertIn(response.status_code, (200, 302))
