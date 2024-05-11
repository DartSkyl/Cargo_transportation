from loader import dp, bot_base, roles_dict
from keyboards import main_executor
from utils.routers_for_roles import executor_router

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


async def ex_main_menu(msg: Message):
    await msg.answer('Пожалуйста, выберете действие:', reply_markup=main_executor)
