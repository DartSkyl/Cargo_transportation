from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


main_all_roles = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть доступные заказы')],
    [KeyboardButton(text='Создать заказ')],
    [KeyboardButton(text='Мои заказы')]
], resize_keyboard=True)