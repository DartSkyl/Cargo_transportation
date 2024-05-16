from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder


role_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚛 Исполнитель', callback_data='r_executor')],
    [InlineKeyboardButton(text='📦 Заказчик', callback_data='r_customer')],
    [InlineKeyboardButton(text='➕ Исполнитель + Заказчик', callback_data='r_all_roles')]
])

confirm_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm')],
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='unconfirmed')]
])

make_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить заказ', callback_data='or_confirm')],
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='or_unconfirmed')]
])

confirm_order_remove = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да', callback_data='rem_yes')],
    [InlineKeyboardButton(text='⛔ Нет', callback_data='rem_no')]
])

confirm_firm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да', callback_data='yes')],
    [InlineKeyboardButton(text='⛔ Нет', callback_data='no')]
])

confirm_delivery_yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data='con_dev_yes')],
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='con_dev_no')]
])

fith_or_representative = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👨 Физическое лицо', callback_data='pom_fith')],
    [InlineKeyboardButton(text='👨‍✈️ Представитель фирмы', callback_data='pom_repr')]
])


def remove_order(order_id, status):
    if not status:
        rem_kb = InlineKeyboardBuilder()
        rem_kb.button(text='❌ Отменить заказ', callback_data=f'rem_{order_id}')
        rem_kb.adjust(1)
        return rem_kb.as_markup()
    elif status == 'in_way':
        rem_kb = InlineKeyboardBuilder()
        rem_kb.button(text='📷 Посмотреть фото груза', callback_data=f'get_photo_{order_id}')
        rem_kb.adjust(1)
        return rem_kb.as_markup()
    else:
        return None


def confirm_delivery(order_id):
    con_dev = InlineKeyboardBuilder()
    con_dev.button(text='✔️ Подтвердить доставку', callback_data=f'con_dev_{order_id}')
    con_dev.adjust(1)
    return con_dev.as_markup()


def get_photo_history(photo_id):
    his_kb = InlineKeyboardBuilder()
    his_kb.button(text='📷 Посмотреть фото груза', callback_data=f'history_photo_{photo_id}')
    his_kb.adjust(1)
    return his_kb.as_markup()


