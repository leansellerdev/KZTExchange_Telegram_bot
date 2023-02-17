import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from misc.config_data import load_config

ua = UserAgent().random
headers = {"User-Agent": ua}

config = load_config(".env")
api = config.apis.mig_api
responce = requests.get(api, headers=headers)


def get_buy_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')
    block = soup.find('table')

    usd = block.find_all('td')[0].text
    eur = block.find_all('td')[3].text
    rub = block.find_all('td')[6].text
    kgs = block.find_all('td')[9].text
    gbp = block.find_all('td')[12].text
    cny = block.find_all('td')[15].text
    gold = block.find_all('td')[18].text

    exchanges = {"USD": usd,
                 "EUR": eur,
                 "RUB": rub,
                 "KGS": kgs,
                 "GBP": gbp,
                 "CNY": cny,
                 "GOLD": gold}

    return exchanges


def get_sell_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')
    block = soup.find('table')

    usd = block.find_all('td')[2].text
    eur = block.find_all('td')[5].text
    rub = block.find_all('td')[8].text
    kgs = block.find_all('td')[11].text
    gbp = block.find_all('td')[14].text
    cny = block.find_all('td')[17].text
    gold = block.find_all('td')[20].text

    exchanges = {"USD": usd,
                 "EUR": eur,
                 "RUB": rub,
                 "KGS": kgs,
                 "GBP": gbp,
                 "CNY": cny,
                 "GOLD": gold}

    return exchanges
