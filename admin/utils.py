from setup import super_admin, bot
from services.services import get_text_to_send, get_currency_result_text
import random

values = ["USD", "EUR", "RUB", "KGS", "GBP", "CNY", "GOLD"]


# Admin notification function
async def admin_message_notification(func):
    await bot.send_message(super_admin, text=func,
                           parse_mode='html')


def admin_test():
    random_value = random.choice(values)
    random_int = random.randint(1, 100)

    try:
        get_text_to_send(random_value)
        get_currency_result_text(random_int, random_value)
        return "Все работает"
    except ValueError as ve:
        return f"Что-то сломалось! Ошибка:\n{ve}"
