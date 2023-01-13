from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from misc.config import TOKEN
from exchange_rate import get_sell_rates, get_buy_rates, get_daily_send_rates
from data_base import SQLighter
from emoji import emojize


def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    scheduler = AsyncIOScheduler(timezone='Asia/Almaty')

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

    @dp.message_handler(commands=['info'])
    async def info(message: types.Message):

        await bot.send_message(message.from_user.id,
                               text=f'{emojize(":brain:")}Данный бот покажет тебе актуальный курс валют по '
                                    f'отношению к тенге.\n {emojize(":calendar:")}Ты можешь подписаться на ежедневную '
                                    f'рассылку.\n {emojize(":watch:")}Рассылка осуществляется '
                                    f'в <b>9:00</b>, <b>14:00</b> и <b>18:00</b>'
                                    f' часов по Алматы каждый день.',
                               parse_mode='html')

    @dp.message_handler(commands=['subscribe'])
    async def subscribe(message: types.Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, True)
            await bot.send_message(message.chat.id, "Вы успешно подписались на ежедневную рассылку!")
        elif db.subscriber_exists(message.from_user.id) and db.check_subscription(message.from_user.id):
            await bot.send_message(message.from_user.id, text="Вы уже подписаны на ежедневную рассылку!")
        else:
            db.update_subscription(message.from_user.id, True)
            await bot.send_message(message.chat.id, "Вы успешно подписались на ежедневную рассылку!")

    @dp.message_handler(commands=['unsubscribe'])
    async def unsubscribe(message: types.Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, False)
            await bot.send_message(message.chat.id, "Вы не подписаны на ежедневную рассылку!")
        elif db.subscriber_exists(message.from_user.id) and not db.check_subscription(message.from_user.id):
            await bot.send_message(message.from_user.id, text="Вы уже отписались от ежедневной рассылки!")
        else:
            db.update_subscription(message.from_user.id, False)
            await bot.send_message(message.chat.id, "Вы успешно отписались от ежедневной рассылки!")

    @dp.message_handler(commands=['show_all'])
    async def show_all(message: types.Message):

        daily_rates = get_daily_send_rates()
        txt = ''

        for key, values in daily_rates.items():
            txt += f"<b>{key}</b> : {float(values[0]), float(values[1])}\n"

        await bot.send_message(message.from_user.id,
                               text=f"Покупка/продажа:\n"
                                    f"{txt}",
                               parse_mode='html')

    @dp.message_handler(content_types=["text"])
    async def send_exchange_rates(message: types.Message):

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        sell_rates = get_sell_rates()
        buy_rates = get_buy_rates()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        sell_txt = []
        buy_txt = []

        emoji = emojize(":money_with_wings:")

        for keys, values in sell_rates.items():
            if message.text.upper() == keys:
                sell_txt.append(f'<b>KZT</b>/<b>{keys}</b>: <b>{values}</b>')

        for key, value in buy_rates.items():
            if message.text.upper() == key:
                buy_txt.append(f'<b>KZT</b>/<b>{key}</b>: <b>{value}</b>')

        await bot.send_message(message.chat.id,
                               text=f'{current_time}\n'
                                    f'{emoji}{buy_txt[0]}{emoji}\n'
                                    f'{emoji}{sell_txt[0]}{emoji}',
                               reply_markup=markup,
                               parse_mode='html')

    async def daily_send():

        try:
            chat_ids = db.get_subscription()

            daily_rates = get_daily_send_rates()
            txt = ''

            for chat_id in chat_ids:
                if chat_id[2]:
                    for key, values in daily_rates.items():
                        txt += f"<b>{key}</b> : {float(values[0]), float(values[1])}\n"

                    await bot.send_message(chat_id[1],
                                           text=f"{emojize(':calendar:')}ЕЖЕДНЕВНАЯ РАССЫЛКА{emojize(':calendar:')}\n"
                                                f"Покупка/продажа:\n"
                                                f"{txt}",
                                           parse_mode='html')
                    txt = ''
        except Exception as ex:
            print(ex)

    scheduler.add_job(daily_send, trigger='cron', hour='9', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='14', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='18', minute='00')

    scheduler.start()

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
