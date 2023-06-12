from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from setup import super_admin
from core.admin.utils import get_users_list

admin_router: Router = Router()


@admin_router.message(Command(commands=["get_users"]))
async def send_users_data(message: Message):
    text = await get_users_list()

    if message.from_user.id == super_admin:
        await message.answer(text=text)
