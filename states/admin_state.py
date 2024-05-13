from aiogram.fsm.state import StatesGroup, State


class UserManipulation(StatesGroup):
    ban_user = State()
    unban_user = State()
