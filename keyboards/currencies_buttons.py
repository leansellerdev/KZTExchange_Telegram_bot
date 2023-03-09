"""
Keyboard for work with currencies
"""


from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

# Создаем объект KeyboardBulder'а
currency_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Список с валютами
currency_list = ['🇺🇸 USD', '🇪🇺 EUR', '🇷🇺 RUB', '🇰🇬 KGS', '🇬🇧 GBP', '🇨🇳 CNY', '🧈 GOLD', '🔙 Назад']
buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in currency_list]

# Создаем кнопки
currency_kb_builder.row(*buttons, width=3)
