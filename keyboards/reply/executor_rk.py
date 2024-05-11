from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


main_executor = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть доступные заказы')],
    [KeyboardButton(text='Мои заказы')]
], resize_keyboard=True)
