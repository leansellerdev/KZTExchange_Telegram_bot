from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.state import State, StatesGroup
from redis.asyncio.client import Redis

redis: Redis = Redis(host='localhost', port=6379)
storage: RedisStorage = RedisStorage(redis=redis)


class FSMExchangeRates(StatesGroup):

    """
    Bot states

    choose_action - works when core handled /start command and
    lets user choose 1 of 2 action(subscribe or work with currencies)

    choose_currency - works after user chose "work with currencies" action and
    let him choose the currency

    work_with_currency - works after user chose currency and let him send
    value for next calculations
    """

    choose_action = State()
    choose_district = State()
    getting_contacts = State()
    choose_currency = State()
    work_with_currency = State()
