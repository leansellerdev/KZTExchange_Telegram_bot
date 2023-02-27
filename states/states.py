from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

storage: MemoryStorage = MemoryStorage()


class FSMExchangeRates(StatesGroup):
    choose_currency = State()
    work_with_currency = State()
