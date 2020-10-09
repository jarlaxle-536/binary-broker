from binary_broker.applications.accounts.models import *
import faker

def create_bots():
    bots_present = len([cu for cu in CustomUser.objects.all()
        if cu.is_bot])
    bots_to_create = max(0, BOTS_NUMBER - bots_present)
    print(f'will create {bots_to_create} bots.')
    for i in range(bots_to_create):
        create_bot()

def create_bot():
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

def run():
    create_bots()

FAKER = faker.Faker()

BOTS_NUMBER = 5
