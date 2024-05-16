from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


admin_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔎 Посмотреть всех пользователей')],
    [KeyboardButton(text='🤐 Забанить пользователя'), KeyboardButton(text='😮‍💨 Разбанить пользователя')],
    [KeyboardButton(text='📋 Все заказы'), KeyboardButton(text='📂 Архив закрытых заказов')]
], resize_keyboard=True)
