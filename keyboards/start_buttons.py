from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


start_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

buttons_list = ["Работа с валютами", "Подписаться"]
buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in buttons_list]

start_kb_builder.row(*buttons, width=2)
