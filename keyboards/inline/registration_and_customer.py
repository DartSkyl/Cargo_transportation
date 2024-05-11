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

remove_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить заказ', callback_data='remove_order')]
])

confirm_order_remove = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='rem_yes')],
    [InlineKeyboardButton(text='Нет', callback_data='rem_no')]
])
