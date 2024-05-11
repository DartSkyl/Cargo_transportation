from random import choices
import string

from loader import bot_base
from .order_container import OrderContainer


class OrderBoard:
    """Данный класс реализует доску заказов"""

    def __init__(self):
        self._order_list = list()

    async def add_order(self, customer_id: int,
                        point_of_departure: str,
                        point_of_delivery: str,
                        parcel_contents: str,
                        time_delivery: str,
                        price: str,
                        contacts: str):
        """Добавляем заказ на общую доску и сохраняем в базу"""

        order_id = ''.join(choices(string.digits + string.ascii_letters, k=8))

        order = OrderContainer(
            container_id=order_id,
            customer_id=customer_id,
            point_of_departure=point_of_departure,
            point_of_delivery=point_of_delivery,
            parcel_contents=parcel_contents,
            time_delivery=time_delivery,
            price=price,
            contacts=contacts
        )

        # И сразу пишем в базу
        await bot_base.add_order_in_base(
            container_id=order_id,
            customer_id=customer_id,
            point_of_departure=point_of_departure,
            point_of_delivery=point_of_delivery,
            parcel_contents=parcel_contents,
            time_delivery=time_delivery,
            price=price,
            contacts=contacts
        )

        self._order_list.append(order)

    async def load_orders_from_base(self):
        """Выгружаем заказы из базы"""
        orders_from_base = await bot_base.load_orders_from_base()
        for elem in orders_from_base:
            order = OrderContainer(
                container_id=elem[0],
                customer_id=elem[1],
                executor_id=elem[2],
                point_of_departure=elem[3],
                point_of_delivery=elem[4],
                parcel_contents=elem[5],
                time_delivery=elem[6],
                price=elem[7],
                contacts=elem[8]
            )
            self._order_list.append(order)

    async def get_customer_orders(self, customer_id):
        """Возвращает список заказов принадлежащих конкретному исполнителю"""
        customer_orders = [order for order in self._order_list if order.get_customer_id() == customer_id]
        return customer_orders


board_with_order = OrderBoard()
