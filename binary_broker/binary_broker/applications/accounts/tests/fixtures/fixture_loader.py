import json, os

global emails, passwords

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CURRENT_DIR, 'email_pw_fixtures.json')) as file:
    fixtures = json.load(file)
