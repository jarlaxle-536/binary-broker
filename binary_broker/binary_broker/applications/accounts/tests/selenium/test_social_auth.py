from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import json
import os

from binary_broker.applications.accounts.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, '/gecko')
HOST = 'http://localhost:8000'

class SocialAuthTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = initialize_webdriver()
        self.driver.get(HOST)

    def tearDown(self):
        self.driver.quit()

    def social_login(self, provider):
        enter_button = self.driver.find_element_by_id('enter_button')
        enter_button.click()
        provider_auth_button = self.driver.find_element_by_id(
            f'{provider}_auth_btn')
        provider_auth_button.click()

    def test_google_auth(self):
        provider = 'google'
        self.social_login(provider)
        inputs = driver.find_elements_by_tag_name('input')
        for inp in inputs:
            try:
                inp.send_keys(CREDENTIALS[provider]['email'])
                inp.send_keys(Keys.ENTER)
            except: pass

def initialize_webdriver(headless=True):
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    return driver

def get_element(*args, **kwargs):
    return get_elements(*args, **kwargs)[0]

with open('secrets/credentials.json') as file:
    CREDENTIALS = json.load(file)
