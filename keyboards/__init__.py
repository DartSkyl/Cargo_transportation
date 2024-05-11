from .inline.registration_and_customer import role_choice, confirm_choice, remove_order, confirm_order_remove
from .reply.customer_rk import main_customer, confirm_order
from .reply.executor_rk import main_executor
from .reply.all_roles_rk import main_all_roles
from .reply.for_all import cancel_button


__all__ = (

    # Регистрация
    'role_choice',
    'confirm_choice',

    # Заказчики
    'main_customer',
    'confirm_order',
    'remove_order',
    'confirm_order_remove',

    # Исполнители
    'main_executor',

    # Двойная роль
    'main_all_roles',

    # Общие для всех
    'cancel_button'
)
