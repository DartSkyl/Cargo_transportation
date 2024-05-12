from typing import List
from loader import roles_dict
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsCustomerFilter(BaseFilter):
    """Фильтр, проверяющий является ли отправитель сообщения заказчик"""
    def __init__(self, customer_list: List[int]):

        # Список ID заказчиков подгружаем из словаря с ролями
        self.customer_list = customer_list

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.customer_list


class IsExecutorFilter(BaseFilter):
    """Фильтр, проверяющий является ли отправитель сообщения исполнитель"""
    def __init__(self, executor_list: List[int]):

        # Список ID заказчиков подгружаем из словаря с ролями
        self.executor_list = executor_list

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.executor_list


class IsAllRolesFilter(BaseFilter):
    """Фильтр, проверяющий является ли отправитель сообщения исполнитель и заказчиком"""
    def __init__(self, all_roles_list: List[int]):

        # Список ID заказчиков подгружаем из словаря с ролями
        self.all_roles_list = all_roles_list

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.all_roles_list


customer_router = Router()
executor_router = Router()
all_role_router = Router()

# Выше описанные фильтры добавляем прямо в роутер
customer_router.message.filter(IsCustomerFilter(customer_list=roles_dict['customer']))
executor_router.message.filter(IsExecutorFilter(executor_list=roles_dict['executor']))
all_role_router.message.filter(IsAllRolesFilter(all_roles_list=roles_dict['all_roles']))
