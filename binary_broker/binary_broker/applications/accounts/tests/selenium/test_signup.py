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

class SignupTestCase(LiveServerTestCase):

    def setUp(self):
        self.user_data = {
            'email': fixtures['email']['match'],
            'password': fixtures['password']['match']
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.driver = driver
        self.driver.get(HOST)

    def build_data(self, chosen):
        data = dict()
        for k, v in chosen.items():
            key = 'password' if k.startswith('password') else 'email'
            data[k] = fixtures[key][v]
        return data

    def general_signup_test(self, chosen, testing=True):
        data = self.build_data(chosen)
        enter_button = self.driver.find_element_by_id('enter_button')
        enter_button.click()
        auth_window = self.driver.find_element_by_id('auth_window')
        nav_tabs = auth_window.find_element_by_class_name(
            'nav-tabs').find_elements_by_tag_name('li')
        nav_tabs[1].click()
        signup_form = [el for el in auth_window.find_elements_by_tag_name('form')
            if el.text][0]
        inputs_dict = {k: signup_form.find_element_by_id(f'signup_id_{k}')
            for k in ['email', 'password', 'password_confirmation']}
        for k, v in data.items():
            inputs_dict[k].send_keys(v)
        submit_input = signup_form.find_element_by_name('signup')
        submit_input.click()
        error_codes_dict = dict()
        for k, v in chosen.items():
            errors_div = self.driver.find_element_by_id(f'signup_id_{k}_errors')
            list_items = errors_div.find_elements_by_tag_name('li') or []
            error_codes = [li.get_attribute('class').split('code-')[1].split()[0]
                for li in list_items]
            if testing:
                for error_code in ERROR_CODES[k][v]:
                    self.assertIn(error_code, error_codes)
            error_codes_dict[k] = error_codes
        return error_codes_dict

    def test_invalid_email(self):
        self.general_signup_test({
            'email': 'invalid',
            'password': 'no_match',
            'password_confirmation': 'no_match'
        })

    def test_no_match_email(self):
        self.general_signup_test({
            'email': 'no_match',
            'password': 'no_match',
            'password_confirmation': 'no_match'
        })

    def test_match_email(self):
        self.general_signup_test({
            'email': 'match',
            'password': 'no_match',
            'password_confirmation': 'no_match'
        })

    def test_empty_password(self):
        self.general_signup_test({
            'email': 'no_match',
            'password': 'empty',
            'password_confirmation': 'no_match'
        })

    def test_too_short_password(self):
        self.general_signup_test({
            'email': 'no_match',
            'password': 'too_short',
            'password_confirmation': 'no_match'
        })

    def test_passwords_not_same(self):
        all_chosen = [{
            'email': 'no_match',
            'password': pw,
            'password_confirmation': pwc
        } for pw in VALID_PASSWORDS for pwc in VALID_PASSWORDS if pw != pwc]
        for chosen in all_chosen:
            error_codes = self.general_signup_test(chosen, testing=False)
            self.assertIn('passwords_do_not_match',
                error_codes.get('password_confirmation', []))
            self.driver.refresh()

    def test_all_correct(self):
        self.general_signup_test({
            'email': 'no_match',
            'password': 'no_match',
            'password_confirmation': 'no_match'
        })

def initialize_webdriver(headless=True):
    global driver
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)

def get_element(*args, **kwargs):
    return get_elements(*args, **kwargs)[0]

USER_DATA = {
    'email': fixtures['email']['no_match'],
    'password': fixtures['password']['no_match'],
    'password_confirmation': fixtures['password']['no_match']
}
ERROR_CODES = {
    'email': {
        'invalid':
            ['invalid'],
        'no_match':
            [],
        'match':
            ['unique']
    },
    'password': {
        'empty':
            [],
        'too_short':
            ['password_too_short', 'password_too_common', 'password_entirely_numeric'],
        'no_match':
            [],
        'match':
            []
    }
}
ERROR_CODES['password_confirmation'] = ERROR_CODES['password']
VALID_PASSWORDS = ['no_match', 'match']

initialize_webdriver()
