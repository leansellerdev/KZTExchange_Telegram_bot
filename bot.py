from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from misc.config_data import load_config
from models.data_base import SQLighter
from keyboards.currencies_buttons import currency_keyboard
from emoji import emojize
from api.exchange_rate import get_sell_rates, get_buy_rates, get_daily_send_rates


def start_bot():

    config = load_config(".env")
    bot_token = config.tg_bot.token
    super_admin = config.tg_bot.admin_ids[0]

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Asia/Almaty')

    db = SQLighter('db.db')

    """Admin notification function"""

    async def admin_message_notification(user_id: int, name: str):

        await bot.send_message(super_admin, f'Пользователь: <b>{name}</b>,\n'
                                            f'ID: <b>{user_id}</b> сделал запрос',
                               parse_mode='html')

    """Welcome message"""

    @dp.message(Command(commands=['start']))
    async def send_welcome(message: Message):

        user_name = message.from_user.first_name

        await bot.send_message(message.chat.id,
                               text=f"Привет, <b>{user_name}!</b>"
                                    f" Выбери валюту и я отправлю тебе актуальный курс обмена.",
                               reply_markup=currency_keyboard,
                               parse_mode="html")

        await admin_message_notification(message.from_user.id, message.from_user.first_name)

    """Send info"""

    @dp.message(Command(commands=['info']))
    async def info(message: Message):

        await bot.send_message(message.from_user.id,
                               text=f'{emojize(":brain:")}Данный бот покажет тебе актуальный курс валют по '
                                    f'отношению к тенге\n\n {emojize(":calendar:")}Ты можешь подписаться на ежедневную '
                                    f'рассылку\n\n {emojize(":watch:")}Рассылка осуществляется '
                                    f'в <b>9:00</b>, <b>14:00</b> и <b>18:00</b>'
                                    f' часов по Алматы каждый день',
                               parse_mode='html')

    """Subscribe function"""

    @dp.message(Command(commands=['subscribe']))
    async def subscribe(message: Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, True)
            await bot.send_message(message.chat.id, "Вы успешно подписались на ежедневную рассылку!")
        elif db.subscriber_exists(message.from_user.id) and db.check_subscription(message.from_user.id):
            await bot.send_message(message.from_user.id, text="Вы уже подписаны на ежедневную рассылку!")
        else:
            db.update_subscription(message.from_user.id, True)
            await bot.send_message(message.chat.id, "Вы успешно подписались на ежедневную рассылку!")

    """Unsubscribe function"""

    @dp.message(Command(commands=['unsubscribe']))
    async def unsubscribe(message: Message):
        if not db.subscriber_exists(message.from_user.id):
            db.add_subscriber(message.from_user.id, False)
            await bot.send_message(message.chat.id, "Вы не подписаны на ежедневную рассылку!")
        elif db.subscriber_exists(message.from_user.id) and not db.check_subscription(message.from_user.id):
            await bot.send_message(message.from_user.id, text="Вы уже отписались от ежедневной рассылки!")
        else:
            db.update_subscription(message.from_user.id, False)
            await bot.send_message(message.chat.id, "Вы успешно отписались от ежедневной рассылки!")

    """Function for sending all of currencies"""

    @dp.message(Command(commands=['show_all']))
    async def show_all(message: Message):

        daily_rates = get_daily_send_rates()
        txt = ''

        for key, values in daily_rates.items():
            txt += f"<b>{key}</b> : {float(values[0])}, {float(values[1])}\n"

        await bot.send_message(message.from_user.id,
                               text=f"Покупка/продажа:\n"
                                    f"{txt}",
                               parse_mode='html')

    """Sending exchange rates"""

    @dp.message(Text(text=["USD", "EUR", "RUB", "KGS", "GBP", "CNY", "GOLD"],
                     ignore_case=True))
    async def send_exchange_rates(message: Message):

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        sell_rates = get_sell_rates()
        buy_rates = get_buy_rates()

        sell_txt = []
        buy_txt = []

        for keys, values in sell_rates.items():
            if message.text.upper() == keys:
                sell_txt.append(f'<b>KZT/{keys}</b>: <b>{values}₸</b>')

        for key, value in buy_rates.items():
            if message.text.upper() == key:
                buy_txt.append(f'<b>KZT/{key}</b>: <b>{value}₸</b>')

        try:
            await bot.send_message(message.chat.id,
                                   text=f'{current_time}\n'
                                        f'💸{buy_txt[0]}💸\n'
                                        f'💸{sell_txt[0]}💸',
                                   parse_mode='html')
        except Exception as ex:
            print("Это не похоже на валюту", ex)

    """Function for sending exchange rates every day with subscription"""

    async def daily_send():

        try:
            chat_ids = db.get_subscription()

            daily_rates = get_daily_send_rates()

            for chat_id in chat_ids:
                txt = ''
                if chat_id[2]:
                    for key, values in daily_rates.items():
                        txt += f"<b>{key}</b> : {float(values[0])}, {float(values[1])}\n"

                    await bot.send_message(chat_id[1],
                                           text=f"🗓ЕЖЕДНЕВНАЯ РАССЫЛКА🗓\n"
                                                f"Покупка/продажа:\n"
                                                f"{txt}",
                                           parse_mode='html')
        except Exception as ex:
            print(ex)

    scheduler.add_job(daily_send, trigger='cron', hour='9', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='14', minute='00')
    scheduler.add_job(daily_send, trigger='cron', hour='18', minute='00')

    scheduler.start()

    dp.run_polling(bot, skip_updates=True)
