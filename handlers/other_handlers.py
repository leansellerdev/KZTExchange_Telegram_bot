from aiogram import Router
from aiogram.types import Message
from bot_lexicon.lexicon_ru import do_not_understand

router: Router = Router()


# Отлавливаем все мусорные сообщения
@router.message()
async def send_answer(message: Message):
    await message.answer(text=do_not_understand)
