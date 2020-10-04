import json, os

global emails, passwords
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CURRENT_DIR, 'fixtures.json')) as file:
    dct = json.load(file)
    emails, passwords = dct['emails'], dct['passwords']
