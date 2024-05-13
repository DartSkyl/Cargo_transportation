from loader import dp, bot_base
from keyboards import main_all_roles

from aiogram.types import Message
from aiogram import F


async def all_main_menu(msg: Message):
    await msg.answer('Пожалуйста, выберете действие:', reply_markup=main_all_roles)


@dp.message(F.text == '📋 Моя статистика')
async def get_user_stat(msg: Message):
    """Абсолютно для всех вывод статистики от сюда"""
    # user_stat[0] - сколько всего заказов создано/взято
    # user_stat[1] - сколько всего заказов успешно закрыто
    try:
        user_stat = await bot_base.get_user_stat(msg.from_user.id)
        stat_msg = (f'<i>Ваша статистика:</i>\n\n'
                    f'📨 <b>Общее число заказов:</b> {user_stat[0]}\n'
                    f'✔️ <b>Заказов успешно закрыто:</b> {user_stat[1]}\n\n'
                    f'⭐ <b><i>Общий рейтинг:</i></b> {int((user_stat[1] / user_stat[0]) * 100)if user_stat[0] != 0 else 100}')
        await msg.answer(stat_msg)
    except TypeError:  # Если пользователя уже нет в базе
        pass
