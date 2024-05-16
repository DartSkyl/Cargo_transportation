from configuration.config import BOT_TOKEN, BOT_EMAIL, BOT_EMAIL_PASSWORD
from database.base import BotBase
from utils.email_sendler import MailSendler

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token=BOT_TOKEN, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
bot_base = BotBase()
email_sendler = MailSendler(bot_email=BOT_EMAIL, bot_email_password=BOT_EMAIL_PASSWORD)


# Система ролей в боте будет реализована через словарь с тремя ключами.
# Каждый ключ это название роли, который содержит список id юзеров
# принадлежащих к той или иной роли
roles_dict = {
    'executor': [],
    'customer': [],
    'all_roles': []
}

# Черный список содержит тех, кого забанили
blacklist = []


async def base_load():
    """Загружаем базу данных"""
    await bot_base.check_db_structure()


async def load_users():
    """Загружаем зарегистрированных пользователей"""
    users_list = await bot_base.load_user_from_base()  # Получаем список картежей
    for user in users_list:
        # Индекс 0 - id юзера
        # Индекс 1 - роль юзера
        roles_dict[user[1]].append(user[0])


async def start_email_sendler():
    """Запускаем отправителя почты"""
    await email_sendler.start_sendler()
