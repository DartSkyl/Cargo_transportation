from loader import dp, bot_base, roles_dict
from keyboards import main_all_roles
from utils.routers_for_roles import all_role_router

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


async def all_main_menu(msg: Message):
    await msg.answer('Пожалуйста, выберете действие:', reply_markup=main_all_roles)


@dp.message(F.text == 'Моя статистика')
async def get_user_stat(msg: Message):
    """Абсолютно для всех вывод статистики от сюда"""
    # user_stat[0] - сколько всего заказов создано/взято
    # user_stat[1] - сколько всего заказов успешно закрыто

    user_stat = await bot_base.get_user_stat(msg.from_user.id)
    stat_msg = (f'Ваша статистика:\n\n'
                f'Общее число заказов: {user_stat[0]}\n'
                f'Заказов успешно закрыто: {user_stat[1]}\n\n'
                f'Общий рейтинг: {int((user_stat[1] / user_stat[0]) * 100)}')
    await msg.answer(stat_msg)
