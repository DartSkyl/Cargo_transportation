from loader import bot_base


class OrderContainer:
    """Через дынный класс будет реализован объект заказа"""
    def __init__(self,
                 order_num: int,
                 container_id: str,
                 customer_id: int,
                 point_of_departure: str,
                 point_of_delivery: str,
                 parcel_contents: str,
                 time_delivery: str,
                 price: str,
                 contacts: str,
                 need_photo: bool,
                 status=None,
                 executor_id=0,
                 cargo_photo=None):

        self._order_num = order_num
        self._container_id = container_id
        self._customer_id = customer_id
        self._executor_id = executor_id
        self._point_of_departure = point_of_departure
        self._point_of_delivery = point_of_delivery
        self._parcel_contents = parcel_contents
        self._time_delivery = time_delivery
        self._price = price
        self._contacts = contacts
        self._need_photo = need_photo
        self._status = status
        self._cargo_photo = cargo_photo

    def __str__(self):
        self_string = (f'\nNumber: {self._order_num}\n'
                       f'ID: {self._container_id}\n'
                       f'Customer ID: {self._customer_id}\n'
                       f'Executor ID: {self._executor_id}\n'
                       f'Departure: {self._point_of_departure}\n'
                       f'Delivery: {self._point_of_delivery}\n'
                       f'Parcel contents: {self._parcel_contents}\n'
                       f'Time to delivery: {self._time_delivery}\n'
                       f'Price: {self._price}\n'
                       f'Contacts: {self._contacts}\n'
                       f'Status: {self._status}')
        return self_string

    def executor_canceled_order(self):
        """Если исполнитель отменил заказ, то обнуляем executor_id и статус заказа"""
        self._status = None
        self._executor_id = 0

    def set_executor(self, executor_id):
        """Так как, этот метод вызывается только при взятии заказа исполнителем, то метод сразу
        устанавливает ID исполнителя и устанавливает статус заказа take_a_parcel"""

        # Сделаем проверку статуса, что бы избежать одновременного
        # взятия одного заказа несколькими исполнителями

        if not self._status:
            self._executor_id = executor_id
            self._status = 'take_a_parcel'
        else:
            raise ValueError('Заказчик уже назначен!')

    def set_status(self, status):
        """Устанавливаем новый статус заказа. Может принимать значения None, 'take_a_parcel' и 'in_way'"""
        self._status = status

    def set_cargo_photo(self, cargo_photo):
        """Устанавливаем фото груза, которое скинул исполнитель"""
        self._cargo_photo = cargo_photo

    def get_cargo_phot(self):
        """Возвращает file_id фото груза"""
        return self._cargo_photo

    def get_parcel_contents(self):
        """Возвращает строку содержащую информацию о грузе.
        Используется для отправки оповещения заказчика при взятии заказа в исполнении,
        что бы обозначить какой заказ был взят"""
        return self._parcel_contents

    def get_info_for_owner_and_executor(self):
        """Возвращает строку с информацией по заказу для владельца заказа и
        исполнителю заказа, с информацией о статусе и контактах"""
        status_dict = {
            None: 'Открыт',
            'take_a_parcel': 'На пути к пункту отгрузки',
            'in_way': 'В пути к пункту доставки',
            'close': 'Успешно закрыт'
        }
        self_string = (f'<b><i>Заказ №{self._order_num}</i></b>\n\n'
                       f'🚩 <b>Пункт отгрузки:</b> {self._point_of_departure}\n'
                       f'🏁 <b>Пункт доставки:</b> {self._point_of_delivery}\n'
                       f'📦 <b>Описание груза:</b> {self._parcel_contents}\n'
                       f'⌚ <b>Время доставки:</b> {self._time_delivery}\n'
                       f'💵 <b>Вознаграждение:</b> {self._price}\n'
                       f'📞 <b>Контакты:</b> {self._contacts}\n'
                       f'📨 <b>Статус:</b> {status_dict[self._status]}\n'
                       f'📸 <b>Фотоотчет:</b> {"Нужен" if self._need_photo else "Не нужен"}')

        return self_string

    def get_info_for_orders_board(self):
        """Возвращает строку с информацией по заказу для потенциальных исполнителей,
        без информации о статусе и контактах"""
        self_string = (f'<b><i>Заказ №{self._order_num}</i></b>\n\n'
                       f'🚩 <b>Пункт отгрузки:</b> {self._point_of_departure}\n'
                       f'🏁 <b>Пункт доставки:</b> {self._point_of_delivery}\n'
                       f'📦 <b>Описание груза:</b> {self._parcel_contents}\n'
                       f'⌚ <b>Время доставки:</b> {self._time_delivery}\n'
                       f'💵 <b>Вознаграждение:</b> {self._price}\n')

        return self_string

    def get_customer_id(self):
        """Возвращает ID заказчика"""
        return self._customer_id

    def get_executor_id(self):
        """Возвращает ID исполнителя"""
        return self._executor_id

    def get_order_id(self):
        """Возвращает ID заказа"""
        return self._container_id

    def get_order_status(self):
        """Возвращает статус заказа"""
        return self._status

    def get_need_photo(self):
        """Возвращает значение нужно фотоотчет или нет"""
        return self._need_photo

    def edit_order_departure(self, new_departure):
        """Изменяем пункт отгрузки"""
        self._point_of_departure = new_departure
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='point_of_departure',
            variable=new_departure
        )

    def edit_order_delivery(self, new_delivery):
        """Изменить пункт доставки"""
        self._point_of_delivery = new_delivery
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='point_of_delivery',
            variable=new_delivery
        )

    def edit_order_cargo_(self, new_cargo):
        """Изменить описание груза"""
        self._parcel_contents = new_cargo
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='parcel_contents',
            variable=new_cargo
        )

    def edit_order_time(self, new_time):
        """Изменить время доставки"""
        self._time_delivery = new_time
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='time_delivery',
            variable=new_time
        )

    def edit_order_price(self, new_price):
        """Изменить вознаграждение"""
        self._price = new_price
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='price',
            variable=new_price
        )

    def edit_order_contacts(self, new_contacts):
        """Изменить контакты"""
        self._contacts = new_contacts
        bot_base.edit_order_info(
            order_id=self._container_id,
            edit_column='contacts',
            variable=new_contacts
        )

