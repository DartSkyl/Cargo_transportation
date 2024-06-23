from aiogram.fsm.state import StatesGroup, State


class OrderCreating(StatesGroup):
    """Класс стэйтов для создание заказа"""
    departure = State()
    delivery = State()
    parcel_contents = State()
    time_to_delivery = State()
    price = State()
    contacts = State()
    need_photo = State()
    finish = State()
