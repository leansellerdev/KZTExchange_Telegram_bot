"""
Main services
"""


from core.api.api import rates
from datetime import datetime
from core.services.quotes_data import data

data = data.get_data()
mig_rates = data["mig"]

sell_rates = mig_rates["sell"]
buy_rates = mig_rates["buy"]


def daily_send_text():

    daily_rates: dict = data["google"]
    pairs_list: list = []
    for key, value in daily_rates.items():
        pairs_list.append(f"<b>{key.upper()}</b>: {value}\n")

    txt = ''.join(pairs_list)

    return txt


# Function for sending exchange rates every day with subscription
async def daily_send(bot, db):

    chat_ids = db.get_subscription()
    text = daily_send_text()

    for chat_id in chat_ids:
        if chat_id[2]:
            await bot.send_message(chat_id[0],
                                   text=f"🗓ЕЖЕДНЕВНАЯ РАССЫЛКА🗓\n\n"
                                        f"{text}",
                                   parse_mode='html')


def get_text_to_send(value: str):
    current_time = data["update_time"]
    value = value[2:].upper().strip()

    txt = f"{current_time}\nПокупка <b>{value}/KZT</b>: {buy_rates[value]}\nПродажа <b>{value}/KZT</b>: {sell_rates[value]}"

    return txt


def get_rates_to_date_text(day: str):
    current_day = int(datetime.now().strftime("%d"))

    if day == "Позавчера":
        current_day -= 2
    elif day == "Вчера":
        current_day -= 1

    date_to_send = datetime.now().strftime("%Y-%m-") + str(current_day)
    google_rates = rates.get_google_exchange(date_to_send)

    txt = ''

    for key, value in google_rates.items():
        txt += f"<b>{key.upper()}</b>: {value}\n"

    return f"Курс валют за {day}:\n{txt}"


def get_currency_result_text(summa: float, rate: str):
    rate = rate.upper().strip()

    sell = float(sell_rates[rate])
    buy = float(buy_rates[rate])

    result = f"Покупка {summa} <b>{rate}</b> = {int(summa)*buy} <b>KZT</b>\nПродажа {summa} <b>{rate}</b> = {int(summa)*sell} <b>KZT</b>"

    return result
