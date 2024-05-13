import sqlite3


class BotBase:
    """Класс для реализации базы данных и методов для взаимодействия с ней"""

    @staticmethod
    async def check_db_structure():
        """Создаем при первом подключении, а в последующем проверяем, таблицы необходимые для работы бота"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Таблица со всеми юзерами бота. Хранит ID, роль юзера и статистику
            cursor.execute('CREATE TABLE IF NOT EXISTS Users ('
                           'user_id INTEGER PRIMARY KEY,'
                           'user_role TEXT NOT NULL,'
                           'order_created INTEGER DEFAULT 0,'
                           'order_closed INTEGER DEFAULT 0,'
                           'full_name TEXT,'
                           'username TEXT'
                           ');')

            # Таблица с заказами. Хранит ID самого заказа, ID создателя и ID исполнителя.
            # Если ID исполнителя нет, значит заказ еще не взят в работу
            cursor.execute('CREATE TABLE IF NOT EXISTS Orders ('
                           'order_id TEXT PRIMARY KEY,'
                           'customer_id INTEGER NOT NULL,'
                           'executor_id INTEGER DEFAULT 0,'
                           'point_of_departure TEXT,'
                           'point_of_delivery TEXT,'
                           'parcel_contents TEXT,'
                           'time_delivery TEXT,'
                           'price TEXT,'
                           'contacts TEXT,'
                           'status TEXT DEFAULT None,'
                           'cargo_photo TEXT DEFAULT None'
                           ');')
            connection.commit()

    # ========== Методы взаимодействия с заказами ==========

    @staticmethod
    async def add_order_in_base(container_id: str,
                                customer_id: int,
                                point_of_departure: str,
                                point_of_delivery: str,
                                parcel_contents: str,
                                time_delivery: str,
                                price: str,
                                contacts: str):
        """Записываем новый заказ в базу"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute(f'INSERT INTO Orders ('
                           f'order_id,'
                           f'customer_id,'
                           f'point_of_departure,'
                           f'point_of_delivery,'
                           f'parcel_contents,'
                           f'time_delivery,'
                           f'price,'
                           f'contacts'
                           f')'
                           f'VALUES ('
                           f'"{container_id}",'
                           f'{customer_id},'
                           f'"{point_of_departure}",'
                           f'"{point_of_delivery}",'
                           f'"{parcel_contents}",'
                           f'"{time_delivery}",'
                           f'"{price}",'
                           f'"{contacts}"'
                           f');')
            cursor.execute(f'UPDATE Users SET order_created = Users.order_created + 1 WHERE user_id = {customer_id}')
            connection.commit()

    @staticmethod
    async def load_orders_from_base():
        """Выгружаем заказы из базы"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            orders_list = cursor.execute('SELECT * FROM Orders;').fetchall()
            return orders_list

    @staticmethod
    async def remove_order_from_base(order_id: str):
        """Удаление заказа из базы"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM Orders WHERE order_id = "{order_id}"')
            connection.commit()

    @staticmethod
    async def set_executor(order_id: str, executor_id: int):
        """Метод вызывается при назначении исполнителя заказу. По этому сразу меняем статус и executor_id"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE Orders SET executor_id = {executor_id}, status = "take_a_parcel"'
                           f'WHERE order_id = "{order_id}"')
            cursor.execute(f'UPDATE Users SET order_created = Users.order_created + 1 WHERE user_id = {executor_id}')
            connection.commit()

    @staticmethod
    async def executor_taken_cargo(order_id: str, cargo_phot: str):
        """После принятия груза заказчиком добавляем фото в базу и меняем статус"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE Orders SET cargo_photo = "{cargo_phot}", status = "in_way"'
                           f'WHERE order_id = "{order_id}"')
            connection.commit()

    @staticmethod
    async def cancel_execute_order(order_id: str):
        """Метод реализует изменения в базе вызванные отменой заказа исполнителем до получения груза"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE Orders SET executor_id = 0, status = "None"'
                           f'WHERE order_id = "{order_id}"')
            connection.commit()

    @staticmethod
    async def close_order(order_id: str, customer_id: int, executor_id: int):
        """Удаляем заказ из базы и помечаем в статистику заказчику и исполнителю"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM Orders WHERE order_id = "{order_id}"')
            cursor.execute(f'UPDATE Users SET order_closed = Users.order_closed + 1 WHERE user_id = {executor_id}')
            cursor.execute(f'UPDATE Users SET order_closed = Users.order_closed + 1 WHERE user_id = {customer_id}')
            connection.commit()

    # ========== Методы взаимодействия с юзерами ==========

    @staticmethod
    async def load_user_from_base():
        """Выгружаем уже зарегистрированных пользователей из базы"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            users_list = cursor.execute('SELECT * FROM Users;').fetchall()
            return users_list

    @staticmethod
    async def registration_new_user(user_id: int, role: str, full_name: str, username: str):
        """Регистрируем нового пользователя. Передаем его ID и выбранную им роль"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Users (user_id, user_role, full_name, username) '
                           f'VALUES ({user_id}, "{role}", "{full_name}", "{username}");')
            connection.commit()

    @staticmethod
    async def check_user(user_id: int):
        """Проверяем, зарегистрирован пользователь или нет"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            check_result = cursor.execute(f'SELECT * FROM Users WHERE user_id = {user_id};').fetchone()
            return check_result

    @staticmethod
    async def get_user_stat(user_id: int):
        """Возвращает статистику юзера"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            result = cursor.execute(f'SELECT order_created, order_closed'
                                    f' FROM Users WHERE user_id = {user_id};').fetchone()
            return result

    @staticmethod
    async def delete_user(user_id: int):
        """Удаляем пользователя из базы и все его заказы"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM Users WHERE user_id = {user_id}')
            cursor.execute(f'DELETE FROM Orders WHERE customer_id = {user_id}')
            connection.commit()
