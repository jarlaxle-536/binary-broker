from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os

from binary_broker.applications.accounts.tests.fixtures.fixture_loader import *
from binary_broker.applications.accounts.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, '/gecko')
HOST = 'http://localhost:8000'

class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        self.user_data = USER_DATA
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.driver = initialize_webdriver()
        self.driver.get(HOST)

    def tearDown(self):
        self.driver.quit()

    def build_data(self, chosen):
        data = dict()
        for k, v in chosen.items():
            key = 'password' if k.startswith('password') else 'email'
            data[k] = fixtures[key][v]
        return data

    def general_login_test(self, chosen):
        data = self.build_data(chosen)
        enter_button = self.driver.find_element_by_id('enter_button')
        enter_button.click()
        auth_window = self.driver.find_element_by_id('auth_window')
        login_form = [el for el in auth_window.find_elements_by_tag_name('form')
            if el.text][0]
        inputs_dict = {k: login_form.find_element_by_id(f'login_id_{k}')
            for k in ['email', 'password']}
        for k, v in data.items():
            inputs_dict[k].send_keys(v)
        submit_input = login_form.find_element_by_name('login')
        submit_input.click()
        for k, v in chosen.items():
            errors_div = self.driver.find_element_by_id(f'login_id_{k}_errors')
            list_items = errors_div.find_elements_by_tag_name('li') or []
            error_codes = [li.get_attribute('class').split('code-')[1].split()[0]
                for li in list_items]
            print('current error codes:', error_codes)
            print('true error codes:', ERROR_CODES[k][v])
            for error_code in ERROR_CODES[k][v]:
                self.assertIn(error_code, error_codes)

    def test_invalid_email(self):
        self.general_login_test({
            'email': 'invalid',
            'password': 'match'
        })

    def test_invalid_email(self):
        self.general_login_test({
            'email': 'invalid',
            'password': 'match'
        })

    def test_no_match_email(self):
        self.general_login_test({
            'email': 'no_match',
            'password': 'match'
        })

    def test_empty_password(self):
        self.general_login_test({
            'email': 'match',
            'password': 'empty'
        })

    def test_too_short_password(self):
        self.general_login_test({
            'email': 'match',
            'password': 'too_short'
        })

    def test_incorrect_password(self):
        self.general_login_test({
            'email': 'match',
            'password': 'no_match'
        })

    def test_all_correct(self):
        self.general_login_test({
            'email': 'match',
            'password': 'match'
        })

def initialize_webdriver(headless=True):
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    return driver

def get_element(*args, **kwargs):
    return get_elements(*args, **kwargs)[0]

USER_DATA = {
    'email': fixtures['email']['match'],
    'password': fixtures['password']['match']
}
ERROR_CODES = {
    'email': {
        'invalid':
            ['invalid'],
        'no_match':
            ['no_such_user'],
        'match':
            []
    },
    'password': {
        'empty':
            [],
        'too_short':
            ['password_too_short', 'password_too_common', 'password_entirely_numeric'],
        'no_match':
            ['incorrect_password'],
        'match':
            []
    }
}
