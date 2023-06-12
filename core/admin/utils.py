from setup import super_admin, bot
from setup import db


# Admin notification function
async def admin_message_notification(func):
    await bot.send_message(super_admin, text=func,
                           parse_mode='html')


async def get_users_list():

    users = db.get_users()
    text = "Пользователи: \n\n"

    user_counter = 0
    subed_user_counter = 0

    for user in users:

        text += f"ID: {user[0]}\nИмя: {user[1]}\nСтатус: {'Подписан' if user[2] is True else 'Не подписан'}\n\n"

        user_counter += 1

        if user[2]:
            subed_user_counter += 1

    text += f"Общее количество пользователей: {user_counter}\nКоличество подписанных пользователей: {subed_user_counter}"

    return text
