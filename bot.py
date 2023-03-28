"""
This is main file with core configuration, logger, router, database and scheduler
"""


import asyncio
import logging

from setup import *
from core.services.quotes_data import data
from core.services.services import daily_send
from core.handlers import users_handlers, subscription_handlers, other_handlers, admin_handlers, currency_handlers


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting Bot')

    # Регистриуем роутеры в диспетчере
    dp.include_router(admin_handlers.admin_router)
    dp.include_router(users_handlers.router)
    dp.include_router(subscription_handlers.router)
    dp.include_router(currency_handlers.router)
    dp.include_router(other_handlers.router)

    # Собираем информацию о курсах валют и сохраняем ее в файл
    data.save_data()

    # Добавляем задания к планеру
    scheduler.add_job(data.save_data, trigger='cron', hour=8, minute=55)
    scheduler.add_job(daily_send, args=[bot, db], trigger='cron', hour=9, minute=0)
    scheduler.add_job(data.save_data, trigger='cron', hour=13, minute=55)
    scheduler.add_job(daily_send, args=[bot, db], trigger='cron', hour=14, minute=0)
    scheduler.add_job(data.save_data, trigger='cron', hour=17, minute=55)
    scheduler.add_job(daily_send, args=[bot, db], trigger='cron', hour=18, minute=0)

    scheduler.start()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot Stopped!')
