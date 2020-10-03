from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class AuthModalWindowTest(TestCase):

    def test_auth_modal_window_hidden(self):
        """By default, auth modal window should be hidden"""
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        modal_window = bs_object.find('div', {'id': MODAL_WINDOW_ID})
        self.assertEquals(modal_window.get('aria-hidden'), 'true')

MODAL_WINDOW_ID = 'auth_window'
