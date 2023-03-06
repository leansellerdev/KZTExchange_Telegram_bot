from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from setup import super_admin
from admin.utils import admin_test

admin_router: Router = Router()


@admin_router.message(Command(commands=["test"]))
async def send_test_results(message: Message):

    text = admin_test()

    if message.from_user.id == super_admin:
        await message.reply(text=text)
