from misc.config_data import load_config
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Exchange:

    config = load_config(".env")
    ua = UserAgent().random

    def __init__(self):
        self.__google_api = self.config.apis.google_api
        self.__mig_api = self.config.apis.mig_api

        self.__headers = {"User-Agent": self.ua}

    def __get_mig_response(self):
        response = requests.get(self.__mig_api, headers=self.__headers)

        return response.content

    def get_google_exchange(self, date: str):
        currency_dict = {"usd": '',
                         "eur": '',
                         "rub": '',
                         "kgs": '',
                         "gbp": '',
                         "cny": ''}

        for currency in currency_dict.keys():
            responce = requests.get(self.__google_api + f"{date}/currencies/{currency}.json")
            json_data = responce.json()
            currency_dict[currency] = json_data[currency]["kzt"]

        return currency_dict

    def get_mig_exchange(self):
        response = self.__get_mig_response()

        soup = BeautifulSoup(response, 'html.parser')
        block = soup.find('table')
        item = block.find_all('td')

        exchanges = {
            "buy": {
                "USD": item[0].text,
                "EUR": item[3].text,
                "RUB": item[6].text,
                "KGS": item[9].text,
                "GBP": item[12].text,
                "CNY": item[15].text,
                "GOLD": item[18].text
            },
            "sell": {
                "USD": item[2].text,
                "EUR": item[5].text,
                "RUB": item[8].text,
                "KGS": item[11].text,
                "GBP": item[14].text,
                "CNY": item[17].text,
                "GOLD": item[20].text
            }
        }

        return exchanges


rates = Exchange()
