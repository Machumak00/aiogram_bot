import asyncio
import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import utils
from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.crunch import choose_crunch_markup
from loader import dp
from states.CrunchState import CrunchState
from utils.misc import rate_limit, script_wait_message
from utils.misc.files import delete_directory_files
from utils.scripts.crunch import start_crunch
from utils.scripts.crunch.start_crunch import do_key_interrupt


@rate_limit(0.5)
@dp.message_handler(Text(equals=["Crunch"]))
async def crunch_menu(message: types.Message):
    await message.answer("Вы попали в Crunch меню.\n"
                         "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
    await CrunchState.crunch.set()


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.crunch)
async def enter_bruteforce(message: types.Message, state: FSMContext):
    if message.text == 'С шаблоном':
        async with state.proxy() as state_data:
            state_data['is_template'] = True
        await message.answer("Введите длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await CrunchState.pattern_length.set()
    elif message.text == 'Без шаблона':
        async with state.proxy() as state_data:
            state_data['is_template'] = False
        await message.answer("Введите минимальную длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await CrunchState.min_length.set()
    elif message.text == 'RckU':
        await message.answer("Идёт загрузка файлов. Пожалуйста, подождите...")
        await CrunchState.download_files.set()
        pass_path = os.path.dirname(os.path.abspath(utils.scripts.crunch.__file__)) + os.path.sep + 'rcku' + os.path.sep
        files = [open(pass_path + '%d.txt' % i, 'r') for i in range(3)]
        for file in files:
            await message.answer_document(file)
            file.close()
        await message.answer("Все файлы были загружены.")
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@dp.message_handler(state=CrunchState.download_files)
async def enter_password2_1(message: types.Message, state: FSMContext):
    await message.answer("Подождите, файлы ещё загружаются.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.pattern_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        length = int(message.text)
        if length in range(1, 13):
            async with state.proxy() as state_data:
                state_data['min_length'] = length
                state_data['max_length'] = length
            await message.answer("Введите шаблон. Отметьте знаком '@' те символы, которые вы не знаете.\n"
                                 "Пример: если Вы ввели длину пароля 6 и знаете, что цифры 1, 2 и 3 "
                                 "находятся на первом, третьем и шестом местах соответственно, то Ваш "
                                 "ввод будет выглядеть следующим образом: 1@2@@3",
                                 reply_markup=back_menu_markup)
            await CrunchState.symbols.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.symbols)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись назад.\nВведите длину пароля: от 1 до 12 символов.")
        await CrunchState.pattern_length.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif len(message.text) == (await state.get_data())['min_length']:
        async with state.proxy() as state_data:
            state_data['symbols'] = message.text
            await message.answer('Скрипт выполняется...')
            await CrunchState.start_script.set()
            tasks = [
                start_crunch(message.from_user.id, state_data),
                script_wait_message(message)
            ]
            finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            users_data_path = ''
            for task in finished:
                users_data_path = task.result()
            with open(users_data_path + os.path.sep + "passwords.txt") as f:
                await message.answer_document(f)
            delete_directory_files(users_data_path)
            await state.reset_state()
            await message.answer("Скрипт успешно выполнен.\n"
                                 "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверная длина пароля. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.min_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        min_length = int(message.text)
        if min_length in range(1, 13):
            async with state.proxy() as state_data:
                state_data['min_length'] = min_length
            await message.answer("Введите максимальную длину пароля: от 1 до 12 символов.\n"
                                 "Максимальная длина пароля должна быть больше или равна минимальной длины.",
                                 reply_markup=back_menu_markup)
            await CrunchState.max_length.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.max_length)
async def enter_mode(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('min_length')
        await message.answer("Вы вернулись.\n"
                             "Введите минимальную длину пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        max_length = int(message.text)
        if max_length in range(1, 13):
            min_length = (await state.get_data())['min_length']
            if max_length >= min_length:
                async with state.proxy() as state_data:
                    state_data['max_length'] = message.text
                    await message.answer('Скрипт выполняется...')
                    await CrunchState.start_script.set()
                    tasks = [
                        do_key_interrupt(),
                        start_crunch(message.from_user.id, state_data),
                        script_wait_message(message)
                    ]
                    finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in unfinished:
                        task.cancel()
                    for task in finished:
                        if task.result() == True:
                            logging.info('interrupt')
                            await state.reset_state()
                            await message.answer("Скрипт успешно выполнен.\n"
                                                 "Возврат в главное меню. Выберите эксплойт.",
                                                 reply_markup=start_markup)
                            return
                    await asyncio.sleep(5)
                    users_data_path = ''
                    for task in finished:
                        if task.result() != True:
                            users_data_path = task.result()
                    with open(users_data_path + os.path.sep + "passwords.txt") as f:
                        await message.answer_document(f)
                    delete_directory_files(users_data_path)
                    await state.reset_state()
                    await message.answer("Скрипт успешно выполнен.\n"
                                         "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
            else:
                await message.answer("Максимальная длина пароля не может быть меньше минимальной. Попробуйте ещё раз.")
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@dp.message_handler(state=CrunchState.start_script)
async def enter_password2_1(message: types.Message, state: FSMContext):
    await message.answer("Подождите, скрипт ещё выполняется.")
