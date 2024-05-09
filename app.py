import asyncio
import datetime
import handlers  # noqa
from utils.admin_router import admin_router
from loader import dp, bot, base_load, load_users


async def start_up():

    # Для администраторов индивидуальный роутер
    dp.include_router(admin_router)
    # Подключаемся к базе
    await base_load()
    # Выгружаем пользователей
    await load_users()
    # with open('bot.log', 'a') as log_file:
    #     log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')
