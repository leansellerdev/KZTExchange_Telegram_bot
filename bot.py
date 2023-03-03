"""
This is main file with bot configuration, logger, router, database and scheduler
"""


import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from misc.config_data import Config, load_config
from handlers import users_handlers, other_handlers, subscription_handlers, currency_handlers
from models.data_base import SQLighter
from services.services import daily_send
from services.quotes_data import data
from states.states import storage

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Загружаем конфиг в переменную config
config: Config = load_config(".env")
# Инициализируем бот
bot: Bot = Bot(config.tg_bot.token,
               parse_mode='HTML')

# Инициализируем базу данных
db: SQLighter = SQLighter("db.db")

# Создаем объект шедулера
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone='Asia/Almaty')

# Указываем супер-админа
super_admin: config = config.tg_bot.admin_ids[0]


# Admin notification function
async def admin_message_notification(func):
    await bot.send_message(super_admin, text=func,
                           parse_mode='html')


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting Bot')

    # Инициализируем диспетчер
    dp = Dispatcher(storage=storage)

    # Регистриуем роутеры в диспетчере
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
