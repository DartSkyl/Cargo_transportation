from .inline.registration_and_customer import (role_choice, confirm_choice, confirm_delivery_yes_no,
                                               remove_order, confirm_order_remove, confirm_firm, get_photo_history,
                                               confirm_delivery, fith_or_representative, make_order)
from .inline.executer_ik import take_order, confirm_order_taking, taken_order, confirm_a_cancel_taken_order
from .inline.admin_ik import editor_on, editor_panel
from .reply.customer_rk import main_customer
from .reply.executor_rk import main_executor, confirm_cargo_photo
from .reply.all_roles_rk import main_all_roles, history_choice
from .reply.for_all import cancel_button
from .reply.admin_rk import admin_main_menu


__all__ = (

    # Регистрация
    'role_choice',
    'confirm_choice',
    'fith_or_representative',
    'confirm_firm',

    # Заказчики
    'main_customer',
    'make_order',
    'remove_order',
    'confirm_order_remove',
    'confirm_delivery',
    'confirm_delivery_yes_no',
    'get_photo_history',

    # Исполнители
    'main_executor',
    'take_order',
    'confirm_order_taking',
    'taken_order',
    'confirm_a_cancel_taken_order',
    'confirm_cargo_photo',

    # Двойная роль
    'main_all_roles',
    'history_choice',

    # Общие для всех
    'cancel_button',

    # Администратор
    'admin_main_menu',
    'editor_on',
    'editor_panel'
)
