import requests
from bs4 import BeautifulSoup
from config import URL
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {"User-Agent": ua}
responce = requests.get(URL, headers=headers)


def get_sell_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')

    try:
        USD = soup.find_all("td", {"class": "sell delta-neutral"})[0].text
        EUR = soup.find_all("td", {"class": "sell delta-neutral"})[1].text
        RUB = soup.find_all("td", {"class": "sell delta-neutral"})[2].text
        KGS = soup.find_all("td", {"class": "sell delta-neutral"})[3].text
        GBP = soup.find_all("td", {"class": "sell delta-neutral"})[4].text
        CNY = soup.find_all("td", {"class": "sell delta-neutral"})[5].text
        GOLD = soup.find_all("td", {"class": "sell delta-neutral"})[6].text
    except Exception as ex:
        print(ex)
        print('В данный момент невозможно обновить курс, попробуйте позже!')

    EXCHANGES = {"USD": USD,
                 "EUR": EUR,
                 "RUB": RUB,
                 "KGS": KGS,
                 "GBP": GBP,
                 "CNY": CNY,
                 "GOLD": GOLD}

    print('Курс продажи обновлен')

    return EXCHANGES


def get_buy_rates():

    soup = BeautifulSoup(responce.content, 'html.parser')

    try:
        USD = soup.find_all("td", {"class": "buy delta-neutral"})[0].text
        EUR = soup.find_all("td", {"class": "buy delta-neutral"})[1].text
        RUB = soup.find_all("td", {"class": "buy delta-neutral"})[2].text
        KGS = soup.find_all("td", {"class": "buy delta-neutral"})[3].text
        GBP = soup.find_all("td", {"class": "buy delta-neutral"})[4].text
        CNY = soup.find_all("td", {"class": "buy delta-neutral"})[5].text
        GOLD = soup.find_all("td", {"class": "buy delta-neutral"})[6].text
    except Exception as ex:
        print(ex)
        print('В данный момент невозможно обновить курс, попробуйте позже!')

    EXCHANGES = {"USD": USD,
                 "EUR": EUR,
                 "RUB": RUB,
                 "KGS": KGS,
                 "GBP": GBP,
                 "CNY": CNY,
                 "GOLD": GOLD}

    print('Курс покупки обновлен')

    return EXCHANGES
