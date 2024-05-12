from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder


def take_order(order_id):
    take_kb = InlineKeyboardBuilder()
    take_kb.button(text='Принять заказ', callback_data=f'take_{order_id}')
    take_kb.adjust(1)
    return take_kb.as_markup()


confirm_order_taking = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data=f'take_yes')],
    [InlineKeyboardButton(text='Отменить', callback_data=f'take_no')]
])


def taken_order(order_id, status):
    to_kb = InlineKeyboardBuilder()
    if status == 'take_a_parcel':
        to_kb.button(text='Груз принят', callback_data=f'cargo_taken_{order_id}')
        to_kb.button(text='Отменить заказ', callback_data=f'cancel_{order_id}')
    else:
        to_kb.button(text='Груз доставлен', callback_data=f'cargo_delivered_{order_id}')
    to_kb.adjust(1)
    return to_kb.as_markup()


confirm_a_cancel_taken_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='cancel_yes'),
     InlineKeyboardButton(text='Нет', callback_data='cancel_no')]
])
