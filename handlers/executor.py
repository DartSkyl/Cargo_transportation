from loader import roles_dict, bot_base
from keyboards import (main_executor, take_order, confirm_order_taking,
                       taken_order, confirm_a_cancel_taken_order, confirm_cargo_photo, get_photo_history)
from utils.routers_for_roles import executor_router, all_role_router
from utils.order_board import board_with_order
from utils.order_container import OrderContainer
from states import TakenOrder
from .all_roles import all_main_menu

from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext


async def ex_main_menu(msg: Message):
    await msg.answer('Пожалуйста, выберете действие:', reply_markup=main_executor)


@all_role_router.message(F.text == '🔎 Посмотреть доступные заказы')
@executor_router.message(F.text == '🔎 Посмотреть доступные заказы')
async def view_available_orders(msg: Message):
    """Выводит список доступных заказов"""
    available_orders = await board_with_order.get_available_orders(msg.from_user.id)
    if len(available_orders) > 0:
        await msg.answer('<b>Доступные заказы:</b>')
        for order in available_orders:
            await msg.answer(text=order.get_info_for_orders_board(),
                             reply_markup=take_order(order.get_order_id()))
    else:
        await msg.answer('Доступных заказов нет!')


@all_role_router.callback_query(F.data.startswith('take_'))
@executor_router.callback_query(F.data.startswith('take_'))
async def take_the_order(callback: CallbackQuery, state: FSMContext):
    """Заказчик берет заказ, подтверждая свой выбор или нет"""
    if callback.data == 'take_yes':
        try:
            order_id = (await state.get_data())['take_order_id']
            await board_with_order.appoint_an_executor(order_id=order_id, executor_id=callback.from_user.id)
            await callback.message.answer('<b>Заказ принят!</b>\n\nСвяжитесь с заказчиком '
                                          'по указанным в заказе контактам!')
            await callback.message.delete()
            order = await board_with_order.get_order_by_id(order_id)
            order_status = order.get_order_status()  # Отменить заказ можно, если груз еще не получен
            await callback.message.answer(text=order.get_info_for_owner_and_executor(),
                                          # В зависимости от статуса заказа, клавиатура будет разной
                                          reply_markup=taken_order(order_id=order.get_order_id(), status=order_status))
        except ValueError:
            await callback.message.delete()
            await callback.message.answer('К сожалению, данный заказ уже взят другим исполнителем!')

    elif callback.data == 'take_no':
        order_id = (await state.get_data())['take_order_id']
        order = await board_with_order.get_order_by_id(order_id)
        await callback.message.edit_text(text=order.get_info_for_owner_and_executor(),
                                         reply_markup=take_order(order_id))

    else:
        await state.set_data({'take_order_id': callback.data.replace('take_', '')})
        await callback.message.edit_text(text='<b>Подтвердите взятие заказа</b>❗',
                                         reply_markup=confirm_order_taking)


@all_role_router.message(F.text == '📨 История выполненных заказов')
@executor_router.message(F.text == '📂 История заказов')
async def show_executors_history(msg: Message, state: FSMContext):
    """Показываем историю исполнителя"""
    await state.set_data({'': ''})  # Заглушка, что бы задать data
    orders_history_list = await bot_base.get_executor_orders_history(msg.from_user.id)
    if len(orders_history_list) > 0:
        for elem in orders_history_list:
            close_order = OrderContainer(
                order_num=elem[0],
                container_id=elem[1],
                customer_id=elem[2],
                executor_id=elem[3],
                point_of_departure=elem[4],
                point_of_delivery=elem[5],
                parcel_contents=elem[6],
                time_delivery=elem[7],
                price=elem[8],
                contacts=elem[9],
                status=elem[10],
                cargo_photo=elem[11]
            )
            await state.update_data({elem[1]: (elem[11], elem[6])})
            await msg.answer(text=close_order.get_info_for_owner_and_executor(),
                             reply_markup=get_photo_history(elem[1]))
    else:
        await msg.answer('Ваша история пуста!')

    if msg.from_user.id in roles_dict['all_roles']:
        await all_main_menu(msg)


@all_role_router.message(F.text == '🚛 Мои взятые заказы')
@executor_router.message(F.text == '📦 Мои заказы')
async def view_a_orders_in_execute(msg: Message):
    """Выдает список заказов взятых в исполнение"""
    taken_orders = await board_with_order.get_orders_in_execute(msg.from_user.id)
    if len(taken_orders) > 0:
        for order in taken_orders:
            order_status = order.get_order_status()  # Отменить заказ можно, если груз еще не получен
            await msg.answer(text=order.get_info_for_owner_and_executor(),
                             # В зависимости от статуса заказа, клавиатура будет разной
                             reply_markup=taken_order(order_id=order.get_order_id(), status=order_status))
    else:
        await msg.answer('У вас нет активных заказов на доставку!')


@all_role_router.callback_query(F.data.startswith('cargo_taken_'))
@executor_router.callback_query(F.data.startswith('cargo_taken_'))
async def executor_taken_cargo(callback: CallbackQuery, state: FSMContext):
    """Исполнитель сообщает, что приехал в пункт отгрузки.
    После чего он должен скинуть фото груза, который ему передали"""
    await state.set_data({'taken_order_id': callback.data.replace('cargo_taken_', '')})
    await callback.message.delete()
    await callback.message.answer('Скиньте фото, на котором видно весь груз!')
    await state.set_state(TakenOrder.add_photo)


@all_role_router.message(TakenOrder.add_photo)
@executor_router.message(TakenOrder.add_photo)
async def catch_executor_photo(msg: Message, state: FSMContext):
    """Ловим фотографию исполнителя"""
    if msg.photo:
        await state.update_data({'cargo_photo': msg.photo[-1].file_id})
        await msg.answer(text='Теперь нажмите кнопку "Груз получен" или скиньте новое фото.\n'
                              '<b>Заказчику отправиться только то, что вы скинули последним❗</b>',
                         reply_markup=confirm_cargo_photo)


@all_role_router.callback_query(TakenOrder.add_photo, F.data.startswith('add_photo_yes'))
@executor_router.callback_query(TakenOrder.add_photo, F.data.startswith('add_photo_yes'))
async def confirm_executor_photo(callback: CallbackQuery, state: FSMContext):
    """Ждем подтверждения, что груз получен"""
    await callback.answer()
    if callback.data == 'add_photo_yes':
        order = await state.get_data()
        await board_with_order.executor_taken_cargo(
            cargo_photo=order['cargo_photo'],
            order_id=order['taken_order_id']
        )
        await callback.message.answer('Заказчик получил фото и уведомление о том, что вы получили груз')
        order = await board_with_order.get_order_by_id(order['taken_order_id'])
        order_status = order.get_order_status()  # Отменить заказ можно, если груз еще не получен
        await callback.message.answer(text=order.get_info_for_owner_and_executor(),
                                      # В зависимости от статуса заказа, клавиатура будет разной
                                      reply_markup=taken_order(order_id=order.get_order_id(), status=order_status))
        await state.clear()
    elif callback.data == 'add_photo_no':

        # В зависимости от роли, направим юзера в соответствующее главное меню
        if callback.from_user.id in roles_dict['executor']:
            await ex_main_menu(callback.message)
        else:
            await all_main_menu(callback.message)
        await state.clear()


@all_role_router.callback_query(F.data.startswith('cancel_'))
@executor_router.callback_query(F.data.startswith('cancel_'))
async def cancel_taken_order(callback: CallbackQuery, state: FSMContext):
    """Отмена заказа и подтверждение отмены"""
    if callback.data == 'cancel_yes':
        cancel_order_id = (await state.get_data())['cancel_order_id']
        await board_with_order.cancel_order_at_executor(
            order_id=cancel_order_id,
            executor_id=callback.from_user.id
        )
        await callback.message.delete()
        await callback.message.answer(text='Заказ снят с исполнения!')

    elif callback.data == 'cancel_no':
        cancel_order_id = (await state.get_data())['cancel_order_id']
        order = await board_with_order.get_order_by_id(cancel_order_id)
        await callback.message.edit_text(text=order.get_info_for_owner_and_executor(),
                                         reply_markup=taken_order(
                                             order_id=cancel_order_id,
                                             status=order.get_order_status()
                                         ))

    else:
        await state.set_data({'cancel_order_id': callback.data.replace('cancel_', '')})
        await callback.message.edit_text(text='<b>Отменить заказ, вы уверены❓</b>',
                                         reply_markup=confirm_a_cancel_taken_order)


@all_role_router.callback_query(F.data.startswith('cargo_delivered_'))
@executor_router.callback_query(F.data.startswith('cargo_delivered_'))
async def executor_delivered_cargo(callback: CallbackQuery):
    """Здесь исполнитель сообщает о прибытии в пункт доставки"""
    await callback.answer()
    delivered_order_id = callback.data.replace('cargo_delivered_', '')
    await board_with_order.cargo_delivered(delivered_order_id)
    await callback.message.answer('<b><i>Заказчик получил соответствующее уведомление.\n'
                                  'Ожидается подтверждение со стороны заказчика</i></b>❗')


@executor_router.callback_query(F.data.startswith('history_photo_'))
async def get_history_photo_for_executor(callback: CallbackQuery, state: FSMContext):
    """Отправляем фото из закрытого заказа"""
    await callback.answer()
    photo = (await state.get_data())[callback.data.replace('history_photo_', '')]
    await callback.message.answer_photo(
        photo=photo[0],
        caption=f'Фото заказа <b><i>{photo[1]}</i></b>'
    )


@executor_router.message(F.text == '⛔ Отмена')
async def cancel_func(msg: Message, state: FSMContext):
    await ex_main_menu(msg=msg)
    await state.clear()
