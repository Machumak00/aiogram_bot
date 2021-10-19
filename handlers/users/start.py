from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import start_markup
from loader import dp
from utils.misc import rate_limit


@rate_limit(0.5)
@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(text="Добро пожаловать в стартовое меню.\n"
                              "Пожалуйста, выберите эксплойт из меню ниже.", reply_markup=start_markup)
