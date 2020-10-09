from bs4 import BeautifulSoup
import requests

def scrape_exchange_rates():
    text = requests.get(URL).text
    bs_object = BeautifulSoup(text, 'html.parser')
    table = bs_object.find('div', {'class': 'flat-wrapper'}).find('table')
    table_keys = [el.text.strip() for el in table.find('thead').find_all('th')]
    table_entries = [[el.text.strip() for el in el.find_all('td')]
        for el in table.find_all('tr')]
    table_entries = [e for e in table_entries if e]
    exchange_rates = {'EUR': {
        'Currency Name': 'Euro', 'Exchange Rate = 1 EUR': 1
    }}
    exchange_rates = dict()
    for entry in table_entries:
        key = hash_func(entry)
        exchange_rates[key] = {
            k: converters[k](v) for k, v in dict(zip(table_keys, entry)).items()
            if k in converters
        }
    return exchange_rates

URL = 'https://www.iban.com/exchange-rates'
hash_func = lambda entry: entry[0]
converters = {'Currency Name': str, 'Exchange Rate = 1 EUR': float}
