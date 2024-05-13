from loader import dp, bot_base, roles_dict, bot, blacklist
from keyboards import admin_main_menu
from utils.admin_router import admin_router
from utils.order_board import board_with_order
from states import UserManipulation

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


@admin_router.message(Command('admin_panel'))
async def open_admin_menu(msg: Message):
    """Открывает меню администратора"""
    await msg.answer(text='Открыта панель администратора:', reply_markup=admin_main_menu)


@admin_router.message(F.text == '🔎 Посмотреть всех пользователей')
async def get_all_users(msg: Message):
    """Выводит список всех зарегистрированных юзеров"""
    roles = {
        'executor': 'Исполнитель',
        'customer': 'Заказчик',
        'all_roles': 'Исполнитель + Заказчик'
    }
    all_user = await bot_base.load_user_from_base()
    msg_text = 'Список всех пользователей:\n\n'
    for user in all_user:
        msg_text += (f'<b>ID:</b> {user[0]}\n<b>Имя:</b> {user[4]}\n'
                     f'<b>Юзернэйм:</b> {"@" + user[5] if user[5] != "None" else "<i>Отсутствует</i>"}\n'
                     f'<b>Роль:</b> {roles[user[1]]}\n\n')
    await msg.answer(msg_text)


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


@admin_router.message(Command('get_log'))
async def get_bot_log(msg: Message):
    """Команда выгружает в чат файл с логом бота"""
    log_file = FSInputFile('bot.log')
    await msg.answer_document(document=log_file)
