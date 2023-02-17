import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from misc.config_data import Config, load_config
from handlers import users_handlers, other_handlers
from models.data_base import SQLighter
from api.google_exchange_rate import get_google_exchange

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Загружаем конфиг в переменную config
config: Config = load_config(".env")
# Инициализируем бот
bot: Bot = Bot(config.tg_bot.token,
               parse_mode='HTML')

db: SQLighter = SQLighter("db.db")
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone='Asia/Almaty')

super_admin: config = config.tg_bot.admin_ids[0]


# Admin notification function
async def admin_message_notification(func):
    await bot.send_message(super_admin, text=func,
                           parse_mode='html')


# Function for sending exchange rates every day with subscription
async def daily_send():
    try:
        chat_ids = db.get_subscription()

        daily_rates = get_google_exchange("latest")

        for chat_id in chat_ids:
            txt = ''
            if chat_id[2]:
                for key, value in daily_rates.items():
                    txt += f"<b>{key.upper()}</b>: {value}\n"

                await bot.send_message(chat_id[1],
                                       text=f"🗓ЕЖЕДНЕВНАЯ РАССЫЛКА🗓\n"
                                            f"{txt}",
                                       parse_mode='html')
    except Exception as ex:
        print(ex)


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
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(users_handlers.router)
    dp.include_router(other_handlers.router)

    # Добавляем задания к планеру
    scheduler.add_job(daily_send, 'cron', hour=9, minute=0)
    scheduler.add_job(daily_send, 'cron', hour=14, minute=0)
    scheduler.add_job(daily_send, 'cron', hour=23, minute=20)
    scheduler.start()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot Stopped!')
