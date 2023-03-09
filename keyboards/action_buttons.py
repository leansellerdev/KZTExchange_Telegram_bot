"""
Keyboard with action buttons for main menu
"""


from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


start_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
change_currency_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

change_currency_btn = ["🔁 Сменить валюту"]
change_currency_keyboard: list[KeyboardButton] = [KeyboardButton(text=value) for value in change_currency_btn]

start_buttons_list = ["💲Работа с валютами", "📝Подписаться"]
start_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_list]

start_kb_builder.row(*start_buttons, width=2)
change_currency_builder.row(*change_currency_keyboard)
