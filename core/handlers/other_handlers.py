"""
Handle all of unexpected things
"""


from aiogram import Router
from aiogram.types import Message
from core.bot_lexicon.lexicon_ru import do_not_understand

router: Router = Router()


# Отлавливаем все мусорные сообщения
@router.message()
async def send_answer(message: Message):
    await message.answer(text=do_not_understand)
