from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os

from binary_broker.applications.accounts.tests.forms.fixture_loader import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, '/gecko')
HOST = 'http://localhost:8000'

class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        "drop all authentication here"
        driver.refresh()

    def present_links_test(self, page_name, wanted_links):
        page_url = get_url(HOST, reverse(page_name))
        print(page_url)
        driver.get(page_url)
        links = [l.get_property('href')
            for l in driver.find_elements_by_tag_name('a')]
        for wanted in wanted_links:
            self.assertIn(get_url(HOST, reverse(wanted)), links)

    def bltest_main_page(self):
        self.present_links_test('main_page', [
            'main_page',
            'commodity_list'
        ])

    def tfdgest_login(self):
        page_url = get_url(HOST, reverse('main_page'))
        driver.get(page_url)
        enter_button = driver.find_element_by_id('enter_button')
        enter_button.click()
        auth_window = driver.find_element_by_id('auth_window')
        login_tab = get_element(
            auth_window.find_elements_by_tag_name,
            hash_func=lambda el: el.text.lower(),
            condition=lambda text: 'login' in text
        )
        login_tab.click()
        login_form = driver.find_element_by_id('login_form')
        login_inputs = {
            k.text.lower().replace('*', ''):
            k.find_element_by_tag_name('input')
            for k in login_form.find_elements_by_class_name('form-group')
        }
        login_inputs['email'].send_keys(emails['match'])
        login_inputs['password'].send_keys(passwords['match'])
        submit_button = [k for k, v in {
                i: i.get_property('type')
                for i in login_form.find_elements_by_tag_name('input')
            }.items() if v == 'submit'][0]
        submit_button.click()

def initialize_webdriver(headless=True):
    global driver
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)

def get_url(*parts):
    return '/'.join(parts).replace('//', '/').replace('http:/', 'http://')

def get_elements(
    search_func,
    hash_func,
    condition,
    *search_args
    ):
    dct = {el: hash_func(el) for el in search_func(*search_args)}
    elements = [k for k, v in dct.items() if condition(v)]
    return elements

def get_element(*args, **kwargs):
    return get_elements(*args, **kwargs)[0]

#initialize_webdriver(headless=False)
