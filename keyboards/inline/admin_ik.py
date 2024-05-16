from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder


def editor_on(order_id):
    editor = InlineKeyboardBuilder()
    editor.button(text='Редактировать', callback_data=f'edit_{order_id}')
    return editor.as_markup()


editor_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить пункт отгрузки', callback_data='edit_departure')],
    [InlineKeyboardButton(text='Изменить пункт Доставки', callback_data='edit_delivery')],
    [InlineKeyboardButton(text='Изменить описание груза', callback_data='edit_cargo')],
    [InlineKeyboardButton(text='Изменить время доставки', callback_data='edit_time')],
    [InlineKeyboardButton(text='Изменить вознаграждение', callback_data='edit_price')],
    [InlineKeyboardButton(text='Изменить контакты', callback_data='edit_contacts')]
])
