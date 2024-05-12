from .inline.registration_and_customer import (role_choice, confirm_choice, confirm_delivery_yes_no,
                                               remove_order, confirm_order_remove, confirm_delivery)
from .inline.executer_ik import take_order, confirm_order_taking, taken_order, confirm_a_cancel_taken_order
from .reply.customer_rk import main_customer, confirm_order
from .reply.executor_rk import main_executor, confirm_cargo_photo
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
    'confirm_delivery',
    'confirm_delivery_yes_no',

    # Исполнители
    'main_executor',
    'take_order',
    'confirm_order_taking',
    'taken_order',
    'confirm_a_cancel_taken_order',
    'confirm_cargo_photo',

    # Двойная роль
    'main_all_roles',

    # Общие для всех
    'cancel_button'
)
