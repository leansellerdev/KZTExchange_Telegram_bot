from api.api import rates
from datetime import datetime
from services.quotes_data import get_data

data = get_data()


# Function for sending exchange rates every day with subscription
async def daily_send(bot, db):
    try:
        chat_ids = db.get_subscription()

        daily_rates = data["google"]

        for chat_id in chat_ids:
            txt = ''
            if chat_id[2]:
                for key, value in daily_rates.items():
                    txt += f"<b>{key.upper()}</b>: {value}\n"

                await bot.send_message(chat_id[1],
                                       text=f"🗓ЕЖЕДНЕВНАЯ РАССЫЛКА🗓\n"
                                            f"{txt}",
                                       parse_mode='html')
    except Exception as ex:
        print(ex)


def get_text_to_send(value: str):
    current_time = data["update_time"]
    value = value.upper()

    mig_rates = data["mig"]

    sell_rates = mig_rates["sell"]
    buy_rates = mig_rates["buy"]

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