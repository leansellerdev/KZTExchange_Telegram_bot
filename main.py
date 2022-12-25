import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DAY_TIMER, CURRENT_DATE
from exchange_rate import get_sell_rates, get_buy_rates
from data_base import SQLighter


def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    db = SQLighter('db.db')

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):

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

    @dp.message_handler(commands=['subscribe'])
    async def subscribe(message: types.Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, True)
        else:
            db.update_subscription(message.from_user.id, True)

        await bot.send_message(message.chat.id, "Вы успешно подписались на ежедневную рассылку!")

    @dp.message_handler(commands=['unsubscribe'])
    async def unsubscribe(message: types.Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, False)
        else:
            db.update_subscription(message.from_user.id, False)

        await bot.send_message(message.chat.id, "Вы успешно отписались от ежедневной рассылки!")

    @dp.message_handler(content_types=["text"])
    async def send_exchange_rates(message: types.Message):

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
            await message.reply("Something went wrong!")

    async def daily_send(wait_for):
        while True:
            await asyncio.sleep(wait_for)

            chat_ids = db.get_subscription()

            sell_rates = get_sell_rates()
            buy_rates = get_buy_rates()

            for chat_id in chat_ids:
                if chat_id[2]:
                    await bot.send_message(chat_id[1], f"Курс покупки на {CURRENT_DATE}:\n {buy_rates}\n"
                                                       f"Курс продажи на {CURRENT_DATE}:\n {sell_rates}")

    loop = asyncio.get_event_loop()
    loop.create_task(daily_send(DAY_TIMER))
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
