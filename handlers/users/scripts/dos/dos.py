from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from loader import dp
from states import DosState
from utils.misc import rate_limit
from utils.scripts.dos.start_dos import start_dos


@rate_limit(5, key='DoS')
@dp.message_handler(Text(equals=["DoS"]))
async def dos_menu(message: types.Message):
    await message.answer("Вы попали в DoS меню.\n"
                         "Введите IP-адрес.", reply_markup=back_menu_markup)
    await DosState.ip.set()


@dp.message_handler(state=DosState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод IP-адреса. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['ip'] = message.text
    await message.answer("Введите порт.")
    await DosState.port.set()


@dp.message_handler(state=DosState.port)
async def enter_port(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод порта. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['port'] = message.text
    await message.answer("Введите размер данных, которыми хотите провести атаку.")
    await DosState.size.set()


@dp.message_handler(state=DosState.size)
async def enter_size(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод размера данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer("Скрипт выполняется...")
    await start_dos(message.from_user.id, data)
    await message.answer("Скрипт успешно выполнен. Возврат в главное меню.\n"
                         "Выберите эксплойт.", reply_markup=start_markup)
    await state.reset_state()
