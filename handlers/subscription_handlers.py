"""
Handle subscription messages
"""


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text, Command
from database.pg_database import PostgreSQL
from admin.utils import admin_message_notification
from bot_lexicon.lexicon_ru import *

db = PostgreSQL()
router: Router = Router()


@router.message(Command(commands=['subscribe']))
@router.message(Text(text=["📝Подписаться"]))
async def subscribe(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(user_id=message.from_user.id,
                          status=True,
                          user_name=message.from_user.full_name)
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
        db.add_subscriber(user_id=message.from_user.id,
                          user_name=message.from_user.full_name)
        await message.answer(text=not_subed)
    elif db.subscriber_exists(message.from_user.id) and not db.check_subscription(message.from_user.id):
        await message.answer(text=already_unsubed)
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer(text=successful_unsub)
        await admin_message_notification(unsubscribe_notification(message.from_user.full_name,
                                                                  message.from_user.id))
