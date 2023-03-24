from setup import super_admin, bot
from setup import db


# Admin notification function
async def admin_message_notification(func):
    await bot.send_message(super_admin, text=func,
                           parse_mode='html')


def get_users():
    data = db.get_users()

    user_counter = 0
    subed_user_counter = 0

    for user in data:
        user_counter += 1

        if user[2]:
            subed_user_counter += 1

    return f"Общее количество пользователей: {user_counter}\nКоличество подписанных пользователей: {subed_user_counter}"
