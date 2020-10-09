"""
    1. Create some bot users, with creation date ~ one week ago.
    2. Make them trade till current moment.
"""

import datetime
import random
import faker

from binary_broker.applications.accounts.models import *
from binary_broker.applications.trading.models import *
from .scraping_exchange_rates import *

def create_commodities():
    exchange_rates = scrape_exchange_rates()
    for currency in sorted(exchange_rates):
        commodity_info = {
            'name': f'{currency}/EUR',
            'mean_price': exchange_rates[currency]['Exchange Rate = 1 EUR'],
        }
        commodity_info['price'] = commodity_info['mean_price']
        Commodity.objects.get_or_create(**commodity_info)

def create_bots():
    bots_present = len([cu for cu in CustomUser.objects.all()
        if cu.is_bot])
    bots_to_create = max(0, BOTS_NUMBER - bots_present)
    print(f'will create {bots_to_create} bots.')
    for i in range(bots_to_create):
        create_bot_with_profile()

def create_bot_with_profile():
    custom_user_info = {
        'email': FAKER.email(),
        'password': FAKER.password(),
        'is_bot': True,
    }
    bot_custom_user = CustomUser.objects.create_user(**custom_user_info)
    profile = bot_custom_user.profile
    profile.first_name = FAKER.first_name()
    profile.last_name = FAKER.last_name()
    profile.country = FAKER.country_code()
    profile.save()

def do_trade():
    actual_time = datetime.datetime.utcnow()
    current_time = actual_time - TIME_TO_PASS
    print(current_time)
    while current_time < actual_time:
        print(current_time)
        current_time += datetime.timedelta(seconds=300*random.random())

def run():
    create_commodities()
    create_bots()
    do_trade()

FAKER = faker.Faker()

BOTS_NUMBER = 5
TIME_TO_PASS = datetime.timedelta(hours=24 * 7)
