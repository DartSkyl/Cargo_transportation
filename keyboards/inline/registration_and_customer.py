from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder


role_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Исполнитель', callback_data='r_executor')],
    [InlineKeyboardButton(text='Заказчик', callback_data='r_customer')],
    [InlineKeyboardButton(text='Исполнитель + Заказчик', callback_data='r_all_roles')]
])

confirm_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='confirm')],
    [InlineKeyboardButton(text='Отмена', callback_data='unconfirmed')]
])
