from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

usd_btn = KeyboardButton(text='USD')
eur_btn = KeyboardButton(text='EUR')
rub_btn = KeyboardButton(text='RUB')
kgs_btn = KeyboardButton(text='KGS')
gbp_btn = KeyboardButton(text='GBP')
cny_btn = KeyboardButton(text='CNY')
gold_btn = KeyboardButton(text='GOLD')

currency_keyboard = ReplyKeyboardMarkup(keyboard=[[usd_btn,
                                                   eur_btn,
                                                   rub_btn,
                                                   kgs_btn,
                                                   gbp_btn,
                                                   cny_btn,
                                                   gold_btn]],
                                        row_width=3, resize_keyboard=True)
