from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from misc.config_data import Config, load_config
from database.pg_database import PostgreSQL
from states.states import storage

# Загружаем конфиг в переменную config
config: Config = load_config(".env")

# Инициализируем бот
bot: Bot = Bot(config.tg_bot.token,
               parse_mode='html')

# Инициализируем базу данных
db: PostgreSQL = PostgreSQL()

# Создаем объект шедулера
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone='Asia/Almaty')

# Указываем супер-админа
super_admin = config.tg_bot.admin_ids[0]

# Инициализируем диспетчер
dp: Dispatcher = Dispatcher(storage=storage)
