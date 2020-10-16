"""
    For the sake of speed, save all bets in local memory (dict, list, ...),
    then batch insert them into db.
"""

import datetime
import random
import faker
import pytz

from django.conf import settings

from binary_broker.applications.accounts.models import *
from binary_broker.applications.trading.models import *
from .scraping_exchange_rates import *

def create_assets():
    exchange_rates = scrape_exchange_rates()
    for currency in sorted(exchange_rates):
        asset_info = {
            'name': f'{currency}/EUR',
            'mean_price': exchange_rates[currency]['Exchange Rate = 1 EUR'],
        }
        asset_info['price'] = asset_info['mean_price']
        Asset.objects.get_or_create(**asset_info)

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
    profile.real_account.havings = 1000 * random.random()
    profile.save()
    profile.real_account.save()

def do_trade():
    utc = pytz.UTC
    users = [u for u in Bot.objects.all()]
    actual_time = utc.localize(datetime.datetime.utcnow())
    current_time = actual_time - TIME_TO_PASS
    while current_time < actual_time:
        print('Current time:', current_time)
        for bet in bot_bets:
            bet.finalize_by_time(current_time)
        print(current_time)
        for asset in assets:
            asset.price = asset.get_new_price()
        for user in users:
            bot_trade(user, current_time)
        current_time += datetime.timedelta(seconds=300 * random.random())

def bot_trade(user, current_time):
    if not user.is_bot: return
    global bot_bets
    chance = 0.1
    will_trade = random.random() < chance
    if will_trade:
        available_ventures = [v for v in settings.BET_VENTURES
            if v[0] <= user.profile.real_account.havings]
        if available_ventures:
            bet_dict = {
                'asset': random.choice(assets),
                'owner': user.profile,
                'is_real_account': True,
                'direction_up': random.choice(settings.BET_DIRECTIONS)[0],
                'venture': random.choice(available_ventures)[0],
                'duration': random.choice(settings.BET_DURATIONS)[0],
            }
            print('user had BEFORE:', user.profile.real_account.havings)
            bet = Bet.objects.create(**bet_dict)
            bet.time_start = current_time
            bet.save()
            print('user has AFTER:', user.profile.real_account.havings)
            bot_bets += [bet]
            print(bet_dict)
            print(bet)
            print(bet.price_when_created)

def run():
    create_assets()
#    global assets, bot_bets
#    assets = Asset.objects.all()
#    bot_bets = list()
#    create_bots()
#    do_trade()

FAKER = faker.Faker()

BOTS_NUMBER = 20
TIME_TO_PASS = datetime.timedelta(minutes=10)
