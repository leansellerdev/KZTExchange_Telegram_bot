"""
Handlers that works with all currencies operations
"""


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from services.services import get_text_to_send, get_currency_result_text
from aiogram.fsm.context import FSMContext
from states.states import FSMExchangeRates
from keyboards.currencies_buttons import currency_kb_builder
from bot_lexicon.lexicon_ru import aq_res
from utils.utils import is_float

router: Router = Router()


@router.message(Text(text=["Работа с валютами"], ignore_case=True), FSMExchangeRates.choose_action)
async def choose_currency(message: Message, state: FSMContext):

    await state.set_state(FSMExchangeRates.choose_currency)
    await message.answer(text=f"Выберите валюту:\n{aq_res}",
                         reply_markup=currency_kb_builder.as_markup(
                             resize_keyboard=True
                         ),
                         parse_mode="html")


@router.message(FSMExchangeRates.choose_action)
async def process_unknown_action(message: Message):
    await message.reply("Выберите действие из списка!")


# Sending exchange rates
@router.message(Text(text=["USD", "EUR", "RUB", "KGS", "GBP", "CNY", "GOLD"],
                     ignore_case=True), FSMExchangeRates.choose_currency)
async def send_exchange_rates(message: Message, state: FSMContext):
    await state.update_data(id=message.from_user.id, rate=message.text)
    await state.set_state(FSMExchangeRates.work_with_currency)
    text = get_text_to_send(message.text)

    await message.answer(text=text, parse_mode="html")
    await message.answer("Введите сумму или выберите другую валюту:")


@router.message(FSMExchangeRates.choose_currency)
async def process_unknown_currency(message: Message):
    await message.reply(text=f"Выберите валюту из списка!\n{aq_res}")


@router.message(FSMExchangeRates.work_with_currency)
async def send_result(message: Message, state: FSMContext):
    data = await state.get_data()
    summa = message.text

    if isinstance(summa, str) and is_float(summa):
        summa = float(summa)
        correct_text = get_currency_result_text(summa=summa, rate=data["rate"])
        await message.answer(text=correct_text,)
    else:
        incorrect_text = "Введите числовое значение!"
        await message.reply(text=f"{incorrect_text}\n",)

    await message.answer(text="Введите сумму или выберите другую валюту:")