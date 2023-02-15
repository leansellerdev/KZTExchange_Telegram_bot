from misc.config_data import API_URL
import requests


def get_api_exchange(date: str):

    currency_dict = {"usd": '',
                     "eur": '',
                     "rub": '',
                     "kgs": '',
                     "gbp": '',
                     "cny": ''}

    for currency in currency_dict.keys():
        responce = requests.get(API_URL + f"{date}/currencies/{currency}.json")
        json_data = responce.json()
        currency_dict[currency] = json_data[currency]["kzt"]

    return currency_dict
