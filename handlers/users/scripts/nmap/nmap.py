import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.nmap.choose_nmap_markup import choose_nmap_markup
from loader import dp
from states import NmapState
from utils.misc import rate_limit
from utils.scripts.nmap.start_nmap import start_nmap


@rate_limit(0.5)
@dp.message_handler(Text(equals=["Nmap"]))
async def nmap_menu(message: types.Message):
    await message.answer("Вы попали в Nmap меню.\n"
                         "Выберите разновидность Nmap.", reply_markup=choose_nmap_markup)
    await NmapState.nmap.set()


@rate_limit(0.5)
@dp.message_handler(state=NmapState.nmap)
async def choose_nmap(message: types.Message, state: FSMContext):
    if message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ['Nmap', 'NmapCustom', 'Vulners', 'VulScan']:
        async with state.proxy() as data:
            data['nmap'] = message.text.lower()
        if message.text == 'NmapCustom':
            await message.answer("Введите доступные команды из списка:"
                                 "[-p, -Pn, -sV, -sS, -A, -O, -F, --open]", reply_markup=back_menu_markup)
            await NmapState.custom_args.set()
        else:
            await message.answer("Введите IP-адрес.", reply_markup=back_menu_markup)
            await NmapState.ip.set()
    else:
        await message.answer('Неверный ввод. Попробуйте другой вариант.')


@rate_limit(0.5)
@dp.message_handler(state=NmapState.custom_args)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('nmap')
        await message.answer("Вы вернулись назад.\nВыберите разновидность Nmap.",
                             reply_markup=choose_nmap_markup)
        await NmapState.nmap.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        arguments = message.text.split()
        in_list = True
        for argument in arguments:
            if argument not in ['-p', '-Pn', '-sV', '-sS', '-A', '-O', '-F', '--open']:
                await message.answer("Неверная команда. Попробуйте ещё раз.")
                in_list = False
                break
        if in_list:
            async with state.proxy() as data:
                data['custom_args'] = message.text
            await message.answer("Введите IP-адрес.")
            await NmapState.ip.set()


@rate_limit(0.5)
@dp.message_handler(state=NmapState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            if 'custom_args' in state_data.keys():
                state_data.pop('custom_args')
                await message.answer("Вы вернулись назад.\nВведите доступные команды из списка.")
                await NmapState.custom_args.set()
            else:
                state_data.pop('nmap')
                await message.answer("Вы вернулись назад.\nВыберите разновидность Nmap.",
                                 reply_markup=choose_nmap_markup)
                await NmapState.nmap.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        async with state.proxy() as data:
            data['ip'] = message.text
            await message.answer('Скрипт выполняется...')
            await NmapState.start_script.set()
            stdout = await start_nmap(data)
            stdout_decoded = stdout.decode('utf-8')
            if data['nmap'] in ['vulscan', 'vulners']:
                if stdout_decoded:
                    await message.answer("Найденные уязвимости:")
                    if len(stdout_decoded) > 4096:
                        for symbols_count in range(0, len(stdout_decoded), 4096):
                            await message.answer(stdout_decoded[symbols_count:symbols_count+4096],
                                                 disable_web_page_preview=True)
                    else:
                        await message.answer(stdout_decoded)
                else:
                    await message.answer("Не было найдено ни одной уязвимости по указанному IP-адресу.")
            else:
                await message.answer(stdout_decoded, disable_web_page_preview=True)
        await message.answer("Скрипт успешно выполнен.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()

@dp.message_handler(state=NmapState.start_script)
async def start_script(message: types.Message, state: FSMContext):
    await message.answer("Подождите, скрипт ещё выполняется.")
