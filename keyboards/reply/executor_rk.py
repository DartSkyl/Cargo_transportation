from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


main_executor = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть доступные заказы')],
    [KeyboardButton(text='Мои заказы'), KeyboardButton(text='Моя статистика')]
], resize_keyboard=True)

confirm_cargo_photo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Груз получен')],
    [KeyboardButton(text='Отмена')]
], resize_keyboard=True)
