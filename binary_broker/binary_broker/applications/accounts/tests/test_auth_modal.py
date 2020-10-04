from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class AuthModalAnonUserTest(TestCase):

    """Unauthorized user auth modal test"""

    def test_auth_modal_window_hidden(self):
        """Anon => main page: auth modal hidden"""
        response = self.client.get(reverse('main_page'))
        bs_object = BeautifulSoup(response.content, 'html.parser')
        modal_window = bs_object.find('div', {'id': MODAL_WINDOW_ID})
        self.assertEquals(modal_window.get('aria-hidden'), 'true')

    def test_auth_modal_window_shown(self):
        """Anon => trading: auth modal pops up"""
        response = self.client.get(reverse('commodity_list'), follow=True)
        bs_object = BeautifulSoup(response.content, 'html.parser')
        modal_window = bs_object.find('div', {'id': MODAL_WINDOW_ID})
        self.assertEquals(modal_window.get('aria-hidden'), 'true')

MODAL_WINDOW_ID = 'auth_window'
