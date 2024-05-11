class OrderContainer:
    """Через дынный класс будет реализован объект заказа"""
    def __init__(self,
                 container_id: str,
                 customer_id: int,
                 point_of_departure: str,
                 point_of_delivery: str,
                 parcel_contents: str,
                 time_delivery: str,
                 price: str,
                 contacts: str,
                 status=None,
                 executor_id=0):

        self._container_id = container_id
        self._customer_id = customer_id
        self._executor_id = executor_id
        self._point_of_departure = point_of_departure
        self._point_of_delivery = point_of_delivery
        self._parcel_contents = parcel_contents
        self._time_delivery = time_delivery
        self._price = price
        self._contacts = contacts
        self._status = status

    def __str__(self):
        self_string = (f'\nID: {self._container_id}\n'
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

    def get_info_for_owner_and_executor(self):
        """Возвращает строку с информацией по заказу для владельца заказа и исполнителю заказа"""
        status_dict = {
            None: 'Открыт',
            'take_a_parcel': 'Забирают груз',
            'in_way': 'В пути к пункту доставки'
        }
        self_string = (f'<b>Пункт отгрузки:</b> {self._point_of_departure}\n'
                       f'<b>Пункт доставки:</b> {self._point_of_delivery}\n'
                       f'<b>Описание груза:</b> {self._parcel_contents}\n'
                       f'<b>Время доставки:</b> {self._time_delivery}\n'
                       f'<b>Вознаграждение:</b> {self._price}\n'
                       f'<b>Контакты:</b> {self._contacts}\n'
                       f'<b>Статус:</b> {status_dict[self._status]}')

        return self_string

    def get_customer_id(self):
        """Возвращает ID заказчика"""
        return self._customer_id
