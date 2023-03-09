"""
Handle all action messages
"""


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from states.states import FSMExchangeRates
from keyboards.action_buttons import start_kb_builder
# from services.services import get_rates_to_date_text
from bot_lexicon.lexicon_ru import *

router: Router = Router()


# Welcome message
@router.message(Command(commands=['start']))
async def start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name

    await state.set_state(FSMExchangeRates.choose_action)
    await message.answer(text=f"Здравствуйте, <b>{user_name}!</b>"
                              f" Выберите действие:",
                         reply_markup=start_kb_builder.as_markup(
                             resize_keyboard=True
                         ),
                         parse_mode="html")


# Send info
@router.message(Command(commands=['info']), FSMExchangeRates.choose_action)
async def info(message: Message):
    await message.answer(text=info_text,
                         parse_mode='html')


@router.message(Text(text=["🔙 Назад"]))
async def get_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.set_state(FSMExchangeRates.choose_action)
    await message.answer(text="Выберите действие:",
                         reply_markup=start_kb_builder.as_markup(
                             resize_keyboard=True
                         ),
                         parse_mode='html')


# Function for sending exchange rates to past days
# @router.message(Text(text=["Позавчера", "Вчера", "Сегодня"],
#                      ignore_case=True))
# async def send_rates_to_date(message: Message):
#     text = get_rates_to_date_text(message.text)
#
#     await message.answer(text=text, parse_mode="html")
