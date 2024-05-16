from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    """Стэйты для регистрации"""
    role_choice = State()
    confirm_choice = State()
    send_email_code = State()
    input_email_code = State()
    input_firm = State()
