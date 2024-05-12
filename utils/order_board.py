from random import choices
import string

from loader import bot_base, roles_dict, bot
from keyboards import confirm_delivery
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

        # После добавления заказа оповещаем всех исполнителей о новом заказе

        for executor in roles_dict['executor']:
            await bot.send_message(chat_id=executor, text='<b>Доступен новый заказ❗</b>')

        for executor in roles_dict['all_roles']:
            # Если заказчик является и исполнителем, то ему сообщение не отправляем
            if executor != customer_id:
                await bot.send_message(chat_id=executor, text='<b>Доступен новый заказ❗</b>')

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
                contacts=elem[8],
                status=elem[9] if elem[9] != 'None' else None,
                cargo_photo=elem[10] if elem[9] != 'None' else None
            )
            self._order_list.append(order)

    async def get_customer_orders(self, customer_id):
        """Возвращает список заказов принадлежащих конкретному исполнителю"""
        customer_orders = [order for order in self._order_list if order.get_customer_id() == customer_id]
        return customer_orders

    async def get_order_by_id(self, order_id):
        """Возвращает объект заказа по ID"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                return order

    async def get_available_orders(self, executor_id):
        """Возвращает список доступных заказов, т.е. заказов со статусом None"""
        available_orders = [order for order in self._order_list
                            # Так же, исключим заказы, которые мог создать исполнитель из роли "заказчик+исполнитель"
                            if not order.get_order_status() and order.get_customer_id() != executor_id]
        return available_orders

    async def get_orders_in_execute(self, executor_id):
        """Возвращает список заказов взятых исполнителем"""
        orders_in_execute = [order for order in self._order_list if order.get_executor_id() == executor_id]
        return orders_in_execute

    async def remove_order(self, order_id):
        """Удаление заказа из доски и из базы через ID заказа"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                self._order_list.remove(order)
                await bot_base.remove_order_from_base(order_id)
                break

    async def appoint_an_executor(self, order_id, executor_id):
        """Метод назначает исполнителя заказу путем назначения executor_id
        и изменением статуса заказа на take_a_parcel. Все одним методом. Так же, заносит изменения в базу.
        Так же оповещает заказчика о взятии заказа в исполнение"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                order.set_executor(executor_id)
                await bot_base.set_executor(order_id=order_id, executor_id=executor_id)
                await bot.send_message(chat_id=order.get_customer_id(),
                                       text=f'Ваш заказ <b>{order.get_parcel_contents()}</b> был взят в исполнение!\n'
                                            f'Исполнитель свяжется с вами в ближайшее время!')
                break

    async def cancel_order_at_executor(self, order_id, executor_id):
        """Исполнитель отменяет заказ взятый в работу. Ставим статус None, executor_id = 0 и сохраняем все в базу.
        Попутно оповещаем заказчика об отказе со стороны исполнителя. Данная функция доступна только если
        исполнитель еще не забрал груз"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                order.executor_canceled_order()
                await bot_base.cancel_execute_order(order_id=order_id)
                await bot.send_message(chat_id=order.get_customer_id(),
                                       text=f'Исполнитель отменил заказ <b>{order.get_parcel_contents()}!</b>\n'
                                            f'Статус заказа изменен на <i>"Открытый"</i>')
                break

    async def executor_taken_cargo(self, cargo_photo, order_id):
        """После того как исполнитель принял груз, он скидывает фото. Так же меняем статус заказа.
        Все изменения заносим в базу и уведомляем заказчика"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                order.set_status(status='in_way')
                order.set_cargo_photo(cargo_photo=cargo_photo)
                await bot_base.executor_taken_cargo(order_id=order_id, cargo_phot=cargo_photo)
                await bot.send_photo(
                    chat_id=order.get_customer_id(),
                    photo=cargo_photo,
                    caption=f'Исполнитель принял груз <b>{order.get_parcel_contents()}</b>\n'
                )
                break

    async def get_cargo_photo(self, order_id):
        """Отправляет фото груза сделанное исполнителем заказчику перевозки"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                await bot.send_photo(
                    chat_id=order.get_customer_id(),
                    photo=order.get_cargo_phot(),
                    caption=f'Груз <b>{order.get_parcel_contents()}</b>\n'
                )
                break

    async def cargo_delivered(self, order_id):
        """Сообщаем заказчику, что груз доставлен и ждем от него подтверждения"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                await bot.send_photo(
                    chat_id=order.get_customer_id(),
                    caption=f'Исполнитель доставил груз <b>{order.get_parcel_contents()}</b>\nПодтвердите получение:',
                    photo=order.get_cargo_phot(),
                    reply_markup=confirm_delivery(order_id)
                )

    async def close_order_successfully(self, order_id):
        """Здесь происходит закрытие заказа, после того как заказчик подтвердил получение груза.
        С последующим удалением из базы и занесением в статистику как исполнителя, так и заказчику"""
        for order in self._order_list:
            if order.get_order_id() == order_id:
                await bot_base.close_order(
                    order_id=order_id,
                    customer_id=order.get_customer_id(),
                    executor_id=order.get_executor_id()
                )
                await bot.send_message(
                    chat_id=order.get_executor_id(),
                    text='<i>Заказчик подтвердил получения груза!</i>'
                )

                # И удаляем из самой доски заказов

                self._order_list.remove(order)
                break


board_with_order = OrderBoard()
