from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


cancel_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='⛔ Отмена')]
], resize_keyboard=True)
