import csv
from loader import bot_base, roles_dict, blacklist
from keyboards import admin_main_menu, editor_on, editor_panel
from utils.admin_router import admin_router
from utils.order_board import board_with_order
from states import UserManipulation, AdminOrderEditor

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


@admin_router.message(Command('admin'))
async def open_admin_menu(msg: Message):
    """Открывает меню администратора"""
    await msg.answer(text='Открыта панель администратора:', reply_markup=admin_main_menu)


@admin_router.message(F.text == '🔎 Посмотреть всех пользователей')
async def get_all_users(msg: Message):
    """Выводит список всех зарегистрированных юзеров"""
    all_user = await bot_base.load_user_from_base()

    table_header = ('ID пользователя', 'Роль', 'Заказов открыто', 'Заказов закрыто',
                    'Имя пользователя', 'Юзернэйм', 'Почта', 'Представительство')

    all_user.insert(0, table_header)  # Вставим шапку таблицы

    with open('users_list.csv', 'w', newline='') as file:
        csv.writer(file).writerows(all_user)

    users = FSInputFile('users_list.csv')
    await msg.answer_document(document=users)


@admin_router.message(F.text == '📂 Архив закрытых заказов')
async def get_orders_archive(msg: Message):
    """Возвращает файл с историей закрытых заказов"""
    orders_history = await bot_base.get_orders_history()

    table_header = ("Номер заказа", "ID заказа", "ID заказчика", "ID исполнителя",
                    "Пункт отгрузки", "Пункт доставки", "Описание груза", "Временной диапазон",
                    "Вознаграждение", "Контакты")

    orders_history.insert(0, table_header)  # Вставим шапку таблицы

    with open('orders_history.csv', 'w', newline='') as file:
        csv.writer(file).writerows(orders_history)

    orders = FSInputFile('orders_history.csv')
    await msg.answer_document(document=orders)


@admin_router.message(F.text == '🤐 Забанить пользователя')
async def start_ban_user(msg:Message, state: FSMContext):
    """Начинаем банить юзера"""
    await state.set_state(UserManipulation.ban_user)
    await msg.answer('Введите ID пользователя, которого хотите заблокировать:')


@admin_router.message(UserManipulation.ban_user)
async def ban_user(msg: Message, state: FSMContext):
    """Баним юзера"""
    if msg.text.isdigit():
        baning_user_id = int(msg.text)
        blacklist.append(baning_user_id)
        await bot_base.delete_user(baning_user_id)

        # Что бы роутеры перестали его воспринимать
        try:
            if baning_user_id in roles_dict['executor']:
                roles_dict['executor'].remove(baning_user_id)
            elif baning_user_id in roles_dict['customer']:
                roles_dict['customer'].remove(baning_user_id)
            else:
                roles_dict['all_roles'].remove(baning_user_id)

            await msg.answer('Пользователь заблокирован!')
            await state.clear()
        except ValueError:
            await msg.answer('Такой пользователь не зарегистрирован!')
    else:
        await msg.answer('ID пользователя должно быть целым числом!')


@admin_router.message(F.text == '😮‍💨 Разбанить пользователя')
async def start_unban_user(msg: Message, state: FSMContext):
    """Начинаем разблокировку пользователя"""
    await state.set_state(UserManipulation.unban_user)
    await msg.answer('Введите ID пользователя, которого хотите разблокировать:')


@admin_router.message(UserManipulation.unban_user)
async def unban_user(msg: Message, state: FSMContext):
    """Разбаним юзера"""
    if msg.text.isdigit():
        try:
            blacklist.remove(int(msg.text))
            await msg.answer('Пользователь разблокирован!')
        except ValueError:
            await msg.answer('Такого юзера нет в черном списке')
    else:
        await msg.answer('ID пользователя должно быть целым числом!')


@admin_router.message(F.text == '📋 Все заказы')
async def view_all_orders(msg: Message):
    """Показывает администратору все заказы с возможностью начать редактирование"""
    all_orders = await board_with_order.get_all_orders()
    for order in all_orders:
        await msg.answer(text=order.get_info_for_owner_and_executor(),
                         reply_markup=editor_on(order_id=order.get_order_id()))


@admin_router.callback_query(F.data.startswith('edit_'))
async def order_editor(callback: CallbackQuery, state: FSMContext):
    """Открываем редактор заказов и вносим изменения"""
    editor_dict = {
        'edit_departure': (AdminOrderEditor.departure, 'Введите новый пункт отгрузки:'),
        'edit_delivery': (AdminOrderEditor.delivery, 'Введите новый пункт доставки:'),
        'edit_cargo': (AdminOrderEditor.cargo, 'Введите новое описание груза:'),
        'edit_time': (AdminOrderEditor.time, 'Введите новое время доставки:'),
        'edit_price': (AdminOrderEditor.price, 'Введите новое вознаграждение:'),
        'edit_contacts': (AdminOrderEditor.contacts, 'Введите новые контакты:')
    }

    try:
        await state.set_state(editor_dict[callback.data][0])
        await callback.message.answer(editor_dict[callback.data][1])

    except KeyError:  # Если пришел коллбэк с ID Заказа
        edit_order = await board_with_order.get_order_by_id(callback.data.replace('edit_', ''))
        await state.set_data({'edit_order': edit_order})
        await callback.message.delete()
        await callback.message.answer(text=edit_order.get_info_for_owner_and_executor(),
                                      reply_markup=editor_panel)


@admin_router.message(AdminOrderEditor.departure)
async def edit_departure(msg: Message, state: FSMContext):
    """Меняем пункт отгрузки"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_departure(new_departure=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(AdminOrderEditor.delivery)
async def edit_delivery(msg: Message, state: FSMContext):
    """Меняем пункт доставки"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_delivery(new_delivery=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(AdminOrderEditor.cargo)
async def edit_cargo(msg: Message, state: FSMContext):
    """Меняем груз"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_cargo_(new_cargo=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(AdminOrderEditor.time)
async def edit_time(msg: Message, state: FSMContext):
    """Меняем время доставки"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_time(new_time=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(AdminOrderEditor.price)
async def edit_price(msg: Message, state: FSMContext):
    """Меняем вознаграждение"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_price(new_price=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(AdminOrderEditor.contacts)
async def edit_contacts(msg: Message, state: FSMContext):
    """Меняем пункт доставки"""
    order_for_editing = (await state.get_data())['edit_order']
    order_for_editing.edit_order_contacts(new_contacts=msg.text)
    await msg.answer('Обновленный заказ:')
    await msg.answer(text=order_for_editing.get_info_for_owner_and_executor(),
                     reply_markup=editor_on(order_for_editing.get_order_id()))


@admin_router.message(Command('get_log'))
async def get_bot_log(msg: Message):
    """Команда выгружает в чат файл с логом бота"""
    log_file = FSInputFile('bot.log')
    await msg.answer_document(document=log_file)
