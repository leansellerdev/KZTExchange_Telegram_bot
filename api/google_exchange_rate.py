from misc.config_data import load_config
import requests

config = load_config(".env")
api = config.apis.google_api


def get_google_exchange(date: str):

    currency_dict = {"usd": '',
                     "eur": '',
                     "rub": '',
                     "kgs": '',
                     "gbp": '',
                     "cny": ''}

    for currency in currency_dict.keys():
        responce = requests.get(api + f"{date}/currencies/{currency}.json")
        json_data = responce.json()
        currency_dict[currency] = json_data[currency]["kzt"]

    return currency_dict
