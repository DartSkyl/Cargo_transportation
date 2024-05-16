from aiogram.fsm.state import StatesGroup, State


class UserManipulation(StatesGroup):
    ban_user = State()
    unban_user = State()


class AdminOrderEditor(StatesGroup):
    departure = State()
    delivery = State()
    cargo = State()
    time = State()
    price = State()
    contacts = State()
