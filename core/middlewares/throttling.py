from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio.client import Redis
from aiogram.fsm.storage.redis import RedisStorage

redis: Redis = Redis(host='redis-throttling', port=6380)
storage_middleware: RedisStorage = RedisStorage(redis)


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self.counter = 0

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user = f'user{event.from_user.id}'

        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if int(check_user.decode()) >= 3:
                await self.storage.redis.set(name=user, value=3, ex=10)
                if self.counter == 0:
                    return
                self.counter = 0
                return await event.answer('Слишком частые запросы. Попробуйте через 10 секунд!')

        self.counter += 1

        await self.storage.redis.set(name=user, value=self.counter, ex=1)

        return await handler(event, data)