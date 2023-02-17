from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

currency_list = ['USD', 'EUR', 'RUB', 'KGS', 'GBP', 'CNY', 'GOLD']
buttons: list[KeyboardButton] = [KeyboardButton(
    text=value) for value in currency_list]

kb_builder.row(*buttons, width=3)

