from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

# Создаем объект KeyboardBulder'а
kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Список с валютами
currency_list = ['USD', 'EUR', 'RUB', 'KGS', 'GBP', 'CNY', 'GOLD']
buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in currency_list]

# Создаем кнопки
kb_builder.row(*buttons, width=3)

