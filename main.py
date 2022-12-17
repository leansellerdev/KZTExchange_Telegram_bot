from datetime import datetime

from telebot.async_telebot import AsyncTeleBot, types
import asyncio
from config import token
from exchange_rate import get_sell_rates, get_buy_rates


def start_bot():
    bot = AsyncTeleBot(token)

    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        user_name = message.from_user.first_name

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        usd = types.KeyboardButton('USD')
        eur = types.KeyboardButton('EUR')
        rub = types.KeyboardButton('RUB')
        kgs = types.KeyboardButton('KGS')
        gbp = types.KeyboardButton('GBP')
        cny = types.KeyboardButton('CNY')
        gold = types.KeyboardButton('GOLD')

        markup.add(usd, eur, rub, kgs, gbp, cny, gold)

        await bot.send_message(message.chat.id,
                               text=f"Привет, <b>{user_name}!</b>"
                                    f" Выбери валюту и я отправлю тебе актуальный курс обмена.",
                               reply_markup=markup,
                               parse_mode="html")

    @bot.message_handler(content_types=["text"])
    async def send_exchange_rates(message):

        sell_rates = get_sell_rates()
        buy_rates = get_buy_rates()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            for key, values in buy_rates.items():
                if message.text.upper() == key:
                    await bot.send_message(message.chat.id,
                                           text=f'Курс покупки <b>KZT</b> к <b>{key}</b> на {current_time}: <b>{values}</b>',
                                           reply_markup=markup,
                                           parse_mode="html")
            for key, values in sell_rates.items():
                if message.text.upper() == key:
                    await bot.send_message(message.chat.id,
                                           text=f'Курс продажи <b>KZT</b> к <b>{key}</b> на {current_time}: <b>{values}</b>',
                                           reply_markup=markup,
                                           parse_mode="html")
        except Exception as ex:
            print(ex)
            await bot.reply_to(message, "Something went wrong!")

    asyncio.run(bot.polling())


if __name__ == '__main__':
    start_bot()
