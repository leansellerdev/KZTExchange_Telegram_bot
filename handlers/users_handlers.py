from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text, Command
from keyboards.currencies_buttons import kb_builder
from bot import db
from bot import admin_message_notification
from services.services import get_text_to_send, get_rates_to_date_text
from bot_lexicon.lexicon_ru import *

router: Router = Router()


# Welcome message
@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    user_name = message.from_user.first_name

    await message.answer(text=f"Привет, <b>{user_name}!</b>"
                              f" Выбери валюту и я отправлю тебе актуальный курс обмена.",
                         reply_markup=kb_builder.as_markup(
                             resize_keyboard=True
                         ),
                         parse_mode="html")

    await admin_message_notification(func=start_notification(message.from_user.full_name,
                                                             message.from_user.id))


# Send info
@router.message(Command(commands=['info']))
async def info(message: Message):
    await message.answer(text=info_text,
                         parse_mode='html')


# Subscribe function
@router.message(Command(commands=['subscribe']))
async def subscribe(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, True)
        await message.answer(text=successful_sub)
        await admin_message_notification(subscribe_notification(message.from_user.full_name,
                                                                message.from_user.id))
    elif db.subscriber_exists(message.from_user.id) and db.check_subscription(message.from_user.id):
        await message.answer(text=already_subed)
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer(text=successful_sub)
        await admin_message_notification(subscribe_notification(message.from_user.full_name,
                                                                message.from_user.id))


# Unsubscribe function
@router.message(Command(commands=['unsubscribe']))
async def unsubscribe(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer(text=not_subed)
    elif db.subscriber_exists(message.from_user.id) and not db.check_subscription(message.from_user.id):
        await message.answer(text=already_unsubed)
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer(text=successful_unsub)
        await admin_message_notification(unsubscribe_notification(message.from_user.full_name,
                                                                  message.from_user.id))


# Function for sending exchange rates to past days
@router.message(Text(text=["Позавчера", "Вчера", "Сегодня"],
                     ignore_case=True))
async def send_rates_to_date(message: Message):
    text = get_rates_to_date_text(message.text)

    await message.answer(text=text, parse_mode="html")


# Sending exchange rates
@router.message(Text(text=["USD", "EUR", "RUB", "KGS", "GBP", "CNY", "GOLD"],
                     ignore_case=True))
async def send_exchange_rates(message: Message):
    text = get_text_to_send(message.text)

    await message.answer(text=text, parse_mode="html")
