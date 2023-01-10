from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from misc.config import TOKEN
from exchange_rate import get_sell_rates, get_buy_rates, get_daily_send_rates
from data_base import SQLighter


def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    scheduler = AsyncIOScheduler(timezone='Asia/Almaty')

    db = SQLighter('db.db')

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

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
            await bot.send_message(message.chat.id, "Вы не подписаны на ежедневную рассылку!")
        else:
            db.update_subscription(message.from_user.id, False)
            await bot.send_message(message.chat.id, "Вы успешно отписались от ежедневной рассылки!")

    @dp.message_handler(content_types=["text"])
    async def send_exchange_rates(message: types.Message):

        try:

            sell_rates = get_sell_rates()
            buy_rates = get_buy_rates()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            for key, values in buy_rates.items():
                if message.text.upper() == key:
                    sell = f'Курс покупки <b>KZT</b> к <b>{key}</b> на {current_time}: <b>{values}</b>'

            for key, values in sell_rates.items():
                if message.text.upper() == key:
                    buy = f'Курс продажи <b>KZT</b> к <b>{key}</b> на {current_time}: <b>{values}</b>'

            await bot.send_message(message.chat.id, text=f'{buy}\n'
                                                         f'{sell}',
                                   reply_markup=markup,
                                   parse_mode='html')

        except Exception as ex:
            print(ex)
            await message.reply("В данный момент невозможно обновить курс валют.\n"
                                "Пожалуйста, попробуйте позже.")

    async def daily_send():

        try:
            chat_ids = db.get_subscription()

            daily_rates = get_daily_send_rates()
            txt = ''

            for chat_id in chat_ids:
                if chat_id[2]:
                    for key, values in daily_rates.items():
                        txt += f"<b>{key}</b> : {values}\n"

                    await bot.send_message(chat_id[1],
                                           text=f"Покупка/продажа:\n"
                                                f"{txt}",
                                           parse_mode='html')
        except Exception as ex:
            print(ex)

    scheduler.add_job(daily_send, trigger='cron', hour='9', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='14', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='18', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='21', minute='00')

    scheduler.start()

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
