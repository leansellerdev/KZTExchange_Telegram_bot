import sqlite3


class SQLighter:

    def __init__(self, database_file):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscription(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'subscriptions' WHERE status = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем есть ли юзер в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'subscriptions' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def check_subscription(self, user_id):
        result = self.cursor.execute("SELECT status FROM 'subscriptions' WHERE user_id = ?", (user_id,)).fetchone()
        return bool(result[0])

    def add_subscriber(self, user_id, status):
        """Добавляем нового юзера"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'subscriptions' (user_id, status) VALUES(?,?)",
                                       (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки"""
        self.cursor.execute("UPDATE 'subscriptions' SET status = ? WHERE user_id = ?",
                            (status, user_id))
        return self.connection.commit()

    def delete_user(self, user_id):
        """Удаляем пользователя из БД"""
        self.cursor.execute("DELETE FROM 'subscriptions' WHERE user_id = (?)", (user_id,))
        return self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
