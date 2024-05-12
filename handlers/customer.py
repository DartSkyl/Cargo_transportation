from keyboards import (main_customer, cancel_button, confirm_order,
                       remove_order, confirm_order_remove, confirm_delivery_yes_no)
from utils.routers_for_roles import customer_router, all_role_router
from utils.order_board import board_with_order
from states.oreder_creating_states import OrderCreating
from .all_roles import all_main_menu
from loader import roles_dict, bot_base

from aiogram.types import Message, CallbackQuery
from aiogram import F, html
from aiogram.fsm.context import FSMContext


async def cust_main_menu(msg: Message):
    await msg.answer(text='Пожалуйста, выберете действие:', reply_markup=main_customer)


# ========== Создание заказа ==========

# Данный функционал общий для ролей "заказчика" и "заказчик + исполнитель"


@all_role_router.message(F.text == '➕ Создать заказ')
@customer_router.message(F.text == '➕ Создать заказ')
async def order_creating(msg: Message, state: FSMContext):
    """Начало создания заказа через специализированный класс"""
    await msg.answer(text='Введите точный адрес, откуда исполнитель должен будет забрать:',
                     reply_markup=cancel_button)
    await state.set_state(OrderCreating.departure)


@all_role_router.message(OrderCreating.departure, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.departure, F.text != '⛔ Отмена')
async def catch_point_of_departure(msg: Message, state: FSMContext):
    """Ловим адрес точки отправки и предлагаем ввести точку доставки"""
    await state.set_data({'departure': msg.text})
    await msg.answer('Теперь введите точный адрес доставки:')
    await state.set_state(OrderCreating.delivery)


@all_role_router.message(OrderCreating.delivery, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.delivery, F.text != '⛔ Отмена')
async def catch_point_of_delivery(msg: Message, state: FSMContext):
    """Ловим адрес доставки и предлагаем ввести содержимое груза"""
    await state.update_data({'delivery': msg.text})
    await msg.answer('Теперь подробно опишите, что необходимо перевезти: содержимое и количество')
    await state.set_state(OrderCreating.parcel_contents)


@all_role_router.message(OrderCreating.parcel_contents, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.parcel_contents, F.text != '⛔ Отмена')
async def catch_parcel_contents(msg: Message, state: FSMContext):
    """Ловим содержимое груза и предлагаем ввести время доставки"""
    await state.update_data({'parcel_contents': msg.text})
    await msg.answer('Укажите время и число к которому нужно доставить груз.\n'
                     'Или диапазон времени (например с 12 до 16):')
    await state.set_state(OrderCreating.time_to_delivery)


@all_role_router.message(OrderCreating.time_to_delivery, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.time_to_delivery, F.text != '⛔ Отмена')
async def catch_time_to_delivery(msg: Message, state: FSMContext):
    """Ловим время доставки и предлагаем ввести цену за доставку"""
    await state.update_data({'time_to_delivery': msg.text})
    await msg.answer('Укажите размер вознаграждения, которе получит доставщик:')
    await state.set_state(OrderCreating.price)


@all_role_router.message(OrderCreating.price, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.price, F.text != '⛔ Отмена')
async def catch_price(msg: Message, state: FSMContext):
    """Ловим цену за доставку и предлагаем ввести контакты"""
    await state.update_data({'price': msg.text})
    await msg.answer('Укажите свой действующий номер телефона и/или другой контакт, '
                     'по которому исполнитель сможет с вами связаться')
    await state.set_state(OrderCreating.contacts)


@all_role_router.message(OrderCreating.contacts, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.contacts, F.text != '⛔ Отмена')
async def catch_contacts_and_show_result(msg: Message, state: FSMContext):
    """Ловим контакты, показываем что в итоге получилось. Дальше заказчик либо все отменяет, либо подтверждает"""

    order_info = await state.get_data()  # Выгружаем все в один словарь
    order_info['contacts'] = msg.text  # И добавляем контакты
    await state.update_data({'contacts': msg.text})  # Так же сохраним для последующей публикации

    msg_text = (f'Предпросмотр:\n\n<b>Пункт отгрузки:</b> {order_info["departure"]}\n'
                f'<b>Пункт доставки:</b> {order_info["delivery"]}\n'
                f'<b>Описание груза:</b> {order_info["parcel_contents"]}\n'
                f'<b>Время доставки:</b> {order_info["time_to_delivery"]}\n'
                f'<b>Вознаграждение за доставку:</b> {order_info["price"]}\n'
                f'<b>Контакты для связи:</b> {order_info["contacts"]}')

    await msg.answer(text=msg_text, reply_markup=confirm_order)
    await state.set_state(OrderCreating.finish)


@all_role_router.message(OrderCreating.finish, F.text != '⛔ Отмена')
@customer_router.message(OrderCreating.finish, F.text != '⛔ Отмена')
async def finish_order_creating(msg: Message, state: FSMContext):
    """Здесь заказчик отправляет на доску заказов, либо отменяет"""
    if msg.text == '📨 Опубликовать заказ':
        order_info = await state.get_data()
        await board_with_order.add_order(
            customer_id=msg.from_user.id,
            point_of_departure=order_info["departure"],
            point_of_delivery=order_info["delivery"],
            parcel_contents=order_info["parcel_contents"],
            time_delivery=order_info["time_to_delivery"],
            price=order_info["price"],
            contacts=order_info["contacts"]
        )
        await msg.answer('Заказ опубликован!')

        # В зависимости от роли, направим юзера в соответствующее главное меню
        if msg.from_user.id in roles_dict['customer']:
            await cust_main_menu(msg=msg)
        else:
            await all_main_menu(msg)
        await state.clear()

    elif msg.text == '❌ Отменить заказ':
        if msg.from_user.id in roles_dict['customer']:
            await cust_main_menu(msg=msg)
        else:
            await all_main_menu(msg)
        await state.clear()


# ========== Просмотр созданных заказов и статистики ==========

# Общая для ролей "заказчик" и "заказчик+исполнитель"
@all_role_router.message(F.text == '📦 Мои созданные заказы')
@customer_router.message(F.text == '📦 Мои заказы')
async def view_customer_orders(msg: Message):
    """Заказчик получает список своих заказов"""
    customer_orders = await board_with_order.get_customer_orders(msg.from_user.id)
    if len(customer_orders) > 0:
        for order in customer_orders:
            order_status = order.get_order_status()  # Удалить заказ можно, только если его еще никто не взял
            order_id = order.get_order_id()
            await msg.answer(text=order.get_info_for_owner_and_executor(),
                             reply_markup=remove_order(
                                 order_id=order_id, status=order_status
                             ))
    else:
        await msg.answer('У вас нет активных заказов!')


@all_role_router.callback_query(F.data.startswith('rem_'))
@customer_router.callback_query(F.data.startswith('rem_'))
async def order_removing(callback: CallbackQuery, state: FSMContext):
    """Запуск удаления заказа, а так же подтверждение или отмена удаления"""
    if callback.data == 'rem_yes':
        order_id = (await state.get_data())['order_id']
        await board_with_order.remove_order(order_id)
        await callback.message.delete()
        await state.clear()

    elif callback.data == 'rem_no':
        order_id = (await state.get_data())['order_id']
        order = await board_with_order.get_order_by_id(order_id)
        order_status = order.get_order_status()  # Удалить заказ можно, только если его еще никто не взял

        await callback.message.edit_text(text=order.get_info_for_owner_and_executor(),
                                         reply_markup=remove_order(
                                             order_id=order_id,
                                             status=order_status
                                         ))
        await state.clear()

    else:
        await state.set_data({'order_id': callback.data.replace('rem_', '')})
        await callback.message.edit_text(text='<b>Вы уверены</b>❓', reply_markup=confirm_order_remove)


@all_role_router.callback_query(F.data.startswith('get_photo_'))
@customer_router.callback_query(F.data.startswith('get_photo_'))
async def get_photo_to_customer(callback: CallbackQuery):
    """После того как исполнитель подтвердил получение груза фото, заказчик может это фото посмотреть в любой момент"""
    await callback.answer()
    await board_with_order.get_cargo_photo(callback.data.replace('get_photo_', ''))


@all_role_router.callback_query(F.data.startswith('con_dev_'))
@customer_router.callback_query(F.data.startswith('con_dev_'))
async def confirm_cargo_delivery_from_customer(callback: CallbackQuery, state: FSMContext):
    """Здесь заказчик подтверждает получение груза"""
    if callback.data == 'con_dev_yes':
        confirming_order_id = (await state.get_data())['confirming_order_id']
        await board_with_order.close_order_successfully(confirming_order_id)
        await callback.answer()
        await callback.message.answer('Заказ успешно закрыт!')
    elif callback.data == 'con_dev_no':
        await callback.message.delete()
    else:
        await callback.answer()
        await state.set_data({'confirming_order_id': callback.data.replace('con_dev_', '')})
        await callback.message.answer(text='<b>Вы уверены</b>❓', reply_markup=confirm_delivery_yes_no)


@all_role_router.message(F.text == '⛔ Отмена')
@customer_router.message(F.text == '⛔ Отмена')
async def cancel_crating_order(msg: Message, state: FSMContext):
    """Отменяем создание заказа и не только"""
    if msg.from_user.id in roles_dict['customer']:
        await cust_main_menu(msg=msg)
    else:
        await all_main_menu(msg)
    await state.clear()

