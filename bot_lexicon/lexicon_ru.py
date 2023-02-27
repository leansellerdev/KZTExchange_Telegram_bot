
# info phrase
info_text = f"""🧠Данный бот покажет тебе актуальный курс валют по 
       отношению к тенге
        \n 📅Ты можешь подписаться на ежедневную рассылку
        \n ⌚Рассылка осуществляется в <b>9:00</b>, <b>14:00</b> и <b>18:00</b>
        часов по Алматы каждый день"""

all_quotes = ["🇺🇸 USD - Доллар США\n",
              "🇪🇺 EUR - Евро\n",
              "🇷🇺 RUB - Российский рубль\n",
              "🇰🇬 KGS - Киргизский сом\n",
              "🇬🇧 GBP - Британский фунт\n",
              "🇨🇳 CNY - Китайский юань\n",
              "🧈 GOLD - Золото"]

aq_res = ''.join(all_quotes)

# subscription phrases
successful_sub = "Вы успешно подписались на ежедневную рассылку!"
already_subed = "Вы уже подписаны на ежедневную рассылку!"
successful_unsub = "Вы успешно отписались от ежедневной рассылки!"
already_unsubed = "Вы уже отписались от ежедневной рассылки!"
not_subed = "Вы не подписаны на ежедневную рассылку!"

do_not_understand = "Простите, я не понимаю"


# subscription notification
def start_notification(name: str, user_id: int):

    return f"Пользователь: <b>{name}</b>,\nID: <b>{user_id}</b> сделал запрос"


def subscribe_notification(name: str, user_id: int):

    return f"Пользователь: <b>{name}</b>,\nID: <b>{user_id}</b> подписался на рассылку"


def unsubscribe_notification(name: str, user_id: int):
    return f"Пользователь: <b>{name}</b>,\nID: <b>{user_id}</b> отписался от рассылки"
