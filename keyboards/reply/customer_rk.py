from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


main_customer = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='➕ Создать заказ'),KeyboardButton(text='📦 Мои заказы')],
    [KeyboardButton(text='📂 История заказов'), KeyboardButton(text='📋 Моя статистика')]
], resize_keyboard=True)
