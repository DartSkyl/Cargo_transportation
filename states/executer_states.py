from aiogram.fsm.state import StatesGroup, State


class TakenOrder(StatesGroup):
    """Стэйты для взятого заказа"""
    add_photo = State()
    confirm_cargo = State()
