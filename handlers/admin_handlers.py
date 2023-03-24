from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from setup import super_admin
from admin.utils import get_users

admin_router: Router = Router()


@admin_router.message(Command(commands=["get_users"]))
async def send_users_data(message: Message):
    text = get_users()

    if message.from_user.id == super_admin:
        await message.reply(text=text)
