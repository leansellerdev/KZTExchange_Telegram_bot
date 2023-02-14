import requests
from bs4 import BeautifulSoup
from misc.config_data import MIG_URL
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {"User-Agent": ua}
responce = requests.get(MIG_URL, headers=headers)


def get_buy_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')
    block = soup.find('table')

    USD = block.find_all('td')[0].text
    EUR = block.find_all('td')[3].text
    RUB = block.find_all('td')[6].text
    KGS = block.find_all('td')[9].text
    GBP = block.find_all('td')[12].text
    CNY = block.find_all('td')[15].text
    GOLD = block.find_all('td')[18].text

    EXCHANGES = {"USD": USD,
                 "EUR": EUR,
                 "RUB": RUB,
                 "KGS": KGS,
                 "GBP": GBP,
                 "CNY": CNY,
                 "GOLD": GOLD}

    print('Курс продажи обновлен')

    return EXCHANGES


def get_sell_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')
    block = soup.find('table')

    USD = block.find_all('td')[2].text
    EUR = block.find_all('td')[5].text
    RUB = block.find_all('td')[8].text
    KGS = block.find_all('td')[11].text
    GBP = block.find_all('td')[14].text
    CNY = block.find_all('td')[17].text
    GOLD = block.find_all('td')[20].text

    EXCHANGES = {"USD": USD,
                 "EUR": EUR,
                 "RUB": RUB,
                 "KGS": KGS,
                 "GBP": GBP,
                 "CNY": CNY,
                 "GOLD": GOLD}

    print('Курс покупки обновлен')

    return EXCHANGES


def get_daily_send_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')
    block = soup.find('table')

    USD = [block.find_all('td')[0].text, block.find_all('td')[2].text]
    EUR = [block.find_all('td')[3].text, block.find_all('td')[5].text]
    RUB = [block.find_all('td')[6].text, block.find_all('td')[8].text]
    KGS = [block.find_all('td')[9].text, block.find_all('td')[11].text]
    GBP = [block.find_all('td')[12].text, block.find_all('td')[14].text]
    CNY = [block.find_all('td')[15].text, block.find_all('td')[17].text]
    GOLD = [block.find_all('td')[18].text, block.find_all('td')[20].text]

    EXCHANGES = {"USD": USD,
                 "EUR": EUR,
                 "RUB": RUB,
                 "KGS": KGS,
                 "GBP": GBP,
                 "CNY": CNY,
                 "GOLD": GOLD}

    return EXCHANGES
