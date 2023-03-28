import datetime

import psycopg2
from core.misc.config_data import load_config

config = load_config(".env")


class PostgreSQL:

    today = datetime.datetime.now().strftime("%d.%m.%Y")

    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(
            host=config.data_base.host,
            user=config.data_base.user,
            password=config.data_base.password,
            database=config.data_base.db_name
        )
        self.cursor = self.connection.cursor()

    def get_server_version(self):
        with self.connection:
            self.cursor.execute(
                "SELECT version();"
            )

            return f"Server version: {self.cursor.fetchone()}"

    def get_subscription(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            self.cursor.execute(
                """SELECT * FROM users WHERE status = (%s);""",
                (status,)
            )

            return self.cursor.fetchall()

    def get_users(self):
        with self.connection:
            self.cursor.execute(
                """SELECT * FROM users;"""
            )

            return self.cursor.fetchall()

    def get_user_reg_date(self, user_id):
        """Получаем дату присоединения пользователя"""
        with self.connection:
            self.cursor.execute(
                """SELECT reg_date FROM users WHERE user_id = (%s)""",
                (user_id,)
            )

            user_reg_date = self.cursor.fetchone()[0]
            return user_reg_date

    def subscriber_exists(self, user_id):
        """Проверяем есть ли юзер в базе"""
        with self.connection:
            self.cursor.execute(
                """SELECT * FROM users WHERE user_id = (%s);""",
                (user_id,)
            )

            result = self.cursor.fetchall()
            return bool(len(result))

    def check_subscription(self, user_id):
        with self.connection:
            self.cursor.execute(
                """SELECT status FROM users WHERE user_id = (%s);""",
                (user_id,)
            )

            result = self.cursor.fetchone()
            return bool(result[0])

    def add_subscriber(self, user_id, user_name, status=False, reg_date=today):
        """Добавляем нового юзера"""
        with self.connection:
            self.cursor.execute(
                """INSERT INTO users (user_id, user_name, status, reg_date)
                   VALUES (%s, %s, %s, %s);""", (user_id, user_name, status, reg_date)
            )

            self.connection.commit()

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки"""
        with self.connection:
            self.cursor.execute(
                """UPDATE users SET status = (%s)
                   WHERE user_id = (%s);""",
                (status, user_id,)
            )

            self.connection.commit()

    def delete_user(self, user_id):
        """Удаляем пользователя из БД"""
        with self.connection:
            self.cursor.execute(
                """DELETE FROM users WHERE user_id = (%s);""",
                (user_id,)
            )

            self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
