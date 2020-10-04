from django.test import TestCase
from django.urls import reverse

class TradingEnterTest(TestCase):

    def test_anon_redirected_to_login(self):
        """Anon trading => login"""
        response = self.client.get(reverse('commodity_list'), follow=True)
        self.assertEquals(response.status_code, 200)
        target_url, *_ = response.redirect_chain[0][0].split('?next')
        self.assertEquals(target_url, reverse('login'))
