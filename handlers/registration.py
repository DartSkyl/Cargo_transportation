from loader import dp, bot_base, roles_dict
from keyboards import role_choice, confirm_choice
from states import Registration
from utils.admin_router import admin_router

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


@dp.message(Command('start'))
async def greetings(msg: Message, state: FSMContext):
    """Приветствие и начало регистрации, либо главное меню роли, если пользователь уже зарегистрирован"""
    # Смотрим, есть ли этот пользователь в базе или нет
    if not await bot_base.check_user(user_id=msg.from_user.id):
        await msg.answer('Добро пожаловать на открытую платформу грузоперевозок!\n'
                         'Выберете свою роль:', reply_markup=role_choice)
        await state.set_state(Registration.role_choice)
    else:
        await msg.answer(text=f'Рады видеть вас снова, <b>{html.quote(msg.from_user.first_name)}</b>!😉')


@dp.callback_query(Registration.role_choice, F.data.startswith('r_'))
async def catch_user_role(callback: CallbackQuery, state: FSMContext):
    """Ловим роль, которую выбрал юзер и ожидаем подтверждения"""
    roles = {
        'r_executor': 'Исполнитель',
        'r_customer': 'Заказчик',
        'r_all_roles': 'Исполнитель + Заказчик'
    }
    await callback.answer()

    # Сохраним выбор пользователя до подтверждения
    await state.set_data({'user_role': callback.data.replace('r_', '')})
    await callback.message.delete()
    await callback.message.answer(text=f'Выбранная роль: <b>{roles[callback.data]}</b>\n'
                                       f'Вы уверены?', reply_markup=confirm_choice)
    await state.set_state(Registration.confirm_choice)


@dp.callback_query(Registration.confirm_choice)
async def confirm_user_choice(callback: CallbackQuery, state: FSMContext):
    """Здесь пользователь подтверждает свой выбор, либо нет"""
    await callback.answer()
    if callback.data == 'confirm':
        user_role = (await state.get_data())['user_role']  # Достаем заранее сохраненный выбор пользователя
        await bot_base.registration_new_user(
            user_id=callback.from_user.id,
            role=user_role
        )
        # Добавляем в словарь по ключу выбранной роли
        roles_dict[user_role].append(callback.from_user.id)
        await callback.message.answer(text='Вы зарегистрированы!')
        await state.clear()
        print(roles_dict)
    else:
        await callback.message.answer(text='Выберете свою роль:', reply_markup=role_choice)
        await state.set_state(Registration.role_choice)


@admin_router.message(Command('get_log'))
async def get_bot_log(msg: Message):
    """Команда выгружает в чат файл с логом бота"""
    log_file = FSInputFile('bot.log')
    await msg.answer_document(document=log_file)
