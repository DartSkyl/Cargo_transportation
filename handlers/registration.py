from smtplib import SMTPRecipientsRefused, SMTPSenderRefused

from loader import dp, bot_base, roles_dict, blacklist, email_sendler
from keyboards import role_choice, confirm_choice
from states import Registration
from .customer import cust_main_menu
from .all_roles import all_main_menu
from .executor import ex_main_menu

from aiogram.types import Message, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

roles = {
    'executor': ('Исполнитель', ex_main_menu),
    'customer': ('Заказчик', cust_main_menu),
    'all_roles': ('Исполнитель + Заказчик', all_main_menu)
}


@dp.message(Command('start'))
async def greetings(msg: Message, state: FSMContext):
    """Приветствие и начало регистрации, либо главное меню роли, если пользователь уже зарегистрирован"""
    # Смотрим, есть ли этот пользователь в базе или нет
    if msg.from_user.id not in blacklist:
        is_user = await bot_base.check_user(user_id=msg.from_user.id)
        if not is_user:
            await msg.answer('Добро пожаловать на открытую платформу грузоперевозок!\n'
                             'Выберете свою роль:', reply_markup=role_choice)
            await state.set_state(Registration.role_choice)
        else:
            await msg.answer(text=f'Рады видеть вас снова, <b>{html.quote(msg.from_user.first_name)}</b>!😉')
            # Открываем главное меню для каждой роли по словарю
            await roles[is_user[1]][1](msg=msg)
            await state.clear()


@dp.callback_query(Registration.role_choice, F.data.startswith('r_'))
async def catch_user_role(callback: CallbackQuery, state: FSMContext):
    """Ловим роль, которую выбрал юзер и ожидаем подтверждения"""

    await callback.answer()

    # Сохраним выбор пользователя до подтверждения
    await state.set_data({'user_role': callback.data.replace('r_', '')})
    await callback.message.delete()
    await callback.message.answer(text=f'Выбранная роль: <b>{roles[callback.data.replace("r_", "")][0]}</b>\n'
                                       f'Вы уверены?', reply_markup=confirm_choice)
    await state.set_state(Registration.confirm_choice)


@dp.callback_query(Registration.confirm_choice)
async def confirm_user_choice(callback: CallbackQuery, state: FSMContext):
    """Здесь пользователь подтверждает свой выбор, либо нет"""
    await callback.answer()
    if callback.data == 'confirm':
        # user_role = (await state.get_data())['user_role']  # Достаем заранее сохраненный выбор пользователя
        # await bot_base.registration_new_user(
        #     user_id=callback.from_user.id,
        #     role=user_role,
        #     full_name=callback.from_user.full_name,
        #     username=callback.from_user.username
        # )
        # # Добавляем в словарь по ключу выбранной роли
        # roles_dict[user_role].append(callback.from_user.id)
        # await callback.message.answer(text='Вы зарегистрированы!')
        # # Открываем главное меню для каждой роли по словарю
        # await roles[user_role][1](msg=callback.message)
        # await state.clear()
        await callback.message.answer('Теперь введите свой e-mail адрес для верификации:')
        await state.set_state(Registration.send_email_code)
    else:
        await callback.message.answer(text='Выберете свою роль:', reply_markup=role_choice)
        await state.set_state(Registration.role_choice)


@dp.message(Registration.send_email_code)
async def send_verification_code(msg: Message, state: FSMContext):
    """Ловим почту пользователя и отправляем туда код подтверждения"""
    try:
        code = await email_sendler.send_verification_code(user_email=msg.text)
        await msg.answer(text='Проверьте почту (в том числе и папку "спам") и введите код подтверждения:')
        await state.update_data({'verification_code': code, 'user_email': msg.text})
        await state.set_state(Registration.input_email_code)
    except SMTPRecipientsRefused:
        await msg.answer('Такого e-mail адреса не существует! Повторите попытку:')
    except UnicodeEncodeError:
        await msg.answer('Такого e-mail адреса не существует! Повторите попытку:')
    except SMTPSenderRefused:
        await msg.answer('Подождите немного и повторите попытку:')


@dp.message(Registration.input_email_code)
async def catch_verification_code(msg: Message, state: FSMContext):
    """Ловим введенный пользователем код проверяем его"""
    user_info = await state.get_data()
    if msg.text == user_info['verification_code']:
        await bot_base.registration_new_user(
            user_id=msg.from_user.id,
            role=user_info['user_role'],
            full_name=msg.from_user.full_name,
            username=msg.from_user.username,
            email=user_info['user_email']
        )
        # Добавляем в словарь по ключу выбранной роли
        roles_dict[user_info['user_role']].append(msg.from_user.id)
        await msg.answer(text='Вы зарегистрированы!')
        # Открываем главное меню для каждой роли по словарю
        await roles[user_info['user_role']][1](msg=msg)
        await state.clear()
    else:
        await msg.answer('Неверный код подтверждения!')
