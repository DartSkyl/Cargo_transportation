import asyncio
import datetime
import handlers  # noqa
from utils.admin_router import admin_router
from utils.routers_for_roles import customer_router, executor_router, all_role_router
from utils.order_board import board_with_order
from loader import dp, bot, base_load, load_users


async def start_up():

    # Для администраторов и всех ролей индивидуальный роутер
    dp.include_router(admin_router)
    dp.include_router(customer_router)
    dp.include_router(executor_router)
    dp.include_router(all_role_router)
    # Подключаемся к базе
    await base_load()
    # Выгружаем пользователей
    await load_users()
    # Выгружаем заказы
    await board_with_order.load_orders_from_base()
    # with open('bot.log', 'a') as log_file:
    #     log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')
