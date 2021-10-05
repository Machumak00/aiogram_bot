import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.dos import choose_dos_markup
from loader import dp
from states import DosState
from utils.misc import rate_limit
from utils.scripts.dos import start_dos, start_nmap, get_ping


@rate_limit(0.5)
@dp.message_handler(Text(equals=["DoS"]))
async def dos_menu(message: types.Message):
    await message.answer("Вы попали в DoS меню.\n"
                         "Выберите способ атаки.", reply_markup=choose_dos_markup)
    await DosState.dos.set()


@rate_limit(0.5)
@dp.message_handler(state=DosState.dos)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ['DoS', 'DoS через Nmap']:
        async with state.proxy() as state_data:
            state_data['dos'] = message.text
        await message.answer("Введите ip.", reply_markup=back_menu_markup)
        await DosState.ip.set()
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=DosState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('dos')
        await message.answer("Вы вернулись назад.\nВыберите способ атаки.", reply_markup=choose_dos_markup)
        await DosState.dos.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        async with state.proxy() as state_data:
            state_data['ip'] = message.text
            if state_data['dos'] == 'DoS':
                await message.answer("Введите порт.")
                await DosState.port.set()
            else:
                ip, ports = await start_nmap(message, state_data)
                if ports == None:
                    await message.answer(
                        "Не было найдено ни одного IP-адреса для DDos-атаки. Попробуйте другой IP-адрес.")
                else:
                    state_data['ports'] = ports
                    await message.answer(f"Nmap нашёл следующие открытые порты. Выберите порты из списка:\n"
                                         f"{ports}")
                    await DosState.port.set()


@rate_limit(0.5)
@dp.message_handler(state=DosState.port)
async def enter_port(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('ip')
        await message.answer("Вы вернулись назад.\nВведите IP.")
        await DosState.ip.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        async with state.proxy() as state_data:
            if 'ports' in state_data.keys():
                if message.text in state_data['ports']:
                    state_data['port'] = message.text
                    await message.answer("Введите размер данных, которыми хотите провести атаку.")
                    await DosState.size.set()
                else:
                    await message.answer("Вы ввели порт не из списка. Попробуйте ещё раз.")
            else:
                state_data['port'] = message.text
                await message.answer("Введите размер данных, которыми хотите провести атаку.")
                await DosState.size.set()
    else:
        await message.answer("Вы ввели не числовое значение. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=DosState.size)
async def enter_size(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('port')
            if 'ports' in state_data.keys():
                await message.answer(f"Вы вернулись назад. Введите порт из списка.\n{state_data['ports']}")
            else:
                await message.answer(f"Вы вернулись назад. Введите порт.")
            await DosState.port.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        async with state.proxy() as state_data:
            state_data['size'] = message.text
            await message.answer("Скрипт выполняется...")
            task1 = asyncio.create_task(get_ping(message, state_data))
            task2 = asyncio.create_task(start_dos(state_data))
            finished, unfinished = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            await message.answer("Скрипт успешно выполнен. Возврат в главное меню.\n"
                                 "Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()
    else:
        await message.answer("Вы ввели не числовое значение. Попробуйте ещё раз.")
